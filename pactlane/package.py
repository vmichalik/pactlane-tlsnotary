"""Package Pactlane TLSNotary from the checksum-verified upstream release."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import tempfile
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.1.0.1501'
VERSION_NAME = VERSION + '-pactlane.2'
UPSTREAM_COMMIT = '68bbd380d6e1a89d79748e5294661c752f5d1205'
DESCRIPTION = 'Create TLSNotary proofs for Pactlane testing.'
ORIGINAL_SHA256 = '1c312ad4305653b8d9351cf3eac46de4222a43be513260bf53053cfa1de45155'
WORKER = '399.bundle.js'
PACKAGE = 'pactlane-tlsnotary-' + VERSION_NAME + '.zip'
CHANGES = (
    ('const g=3e4;', 'const g=6e4;'),
    ('setupProver timed out after 30000ms', 'setupProver timed out after 60000ms'),
    ('setupProverRelay timed out after 30000ms', 'setupProverRelay timed out after 60000ms'),
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prepare(archive, output):
    data = archive.read_bytes()
    if digest(data) != ORIGINAL_SHA256:
        raise SystemExit('Pinned release checksum mismatch; no extension prepared.')
    if output.exists():
        raise SystemExit('Output already exists; choose an unused --output directory. Nothing was overwritten.')

    files = {}
    timestamps = {}
    with zipfile.ZipFile(io.BytesIO(data)) as original:
        for entry in original.infolist():
            name = PurePosixPath(entry.filename)
            if name.is_absolute() or '..' in name.parts or '\\' in entry.filename:
                raise SystemExit('Unexpected archive path; no extension prepared.')
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise SystemExit('Archive links are not supported; no extension prepared.')
            if entry.is_dir():
                continue
            if entry.filename in files:
                raise SystemExit('Duplicate archive entry; no extension prepared.')
            files[entry.filename] = original.read(entry)
            timestamps[entry.filename] = entry.date_time

    if WORKER not in files or 'manifest.json' not in files:
        raise SystemExit('Pinned release layout changed; no extension prepared.')
    before = dict(files)
    text = files[WORKER].decode('utf-8')
    for old, new in CHANGES:
        if text.count(old) != 1:
            raise SystemExit('Pinned worker layout changed; no extension prepared.')
        text = text.replace(old, new, 1)
    files[WORKER] = text.encode('utf-8')

    old_manifest = json.loads(files['manifest.json'])
    if old_manifest.get('version') != VERSION or old_manifest.get('manifest_version') != 3:
        raise SystemExit('Pinned manifest version changed; no extension prepared.')
    manifest = dict(old_manifest)
    manifest['name'] = 'Pactlane TLSNotary'
    manifest['description'] = DESCRIPTION
    manifest['version_name'] = VERSION_NAME
    files['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode('utf-8')
    # Presentation assets only. All executable bundles beyond the existing worker stay byte-identical.
    files['content.styles.css'] = (ROOT / 'packages/extension/src/entries/Content/content.styles.css').read_bytes()
    for name, title in [('confirmPopup.html', 'Pactlane TLSNotary · Review request'), ('options.html', 'Pactlane TLSNotary · Settings')]:
        import re
        html = files[name].decode('utf-8')
        if len(re.findall(r'<title>.*?</title>', html)) != 1 or html.count('</head>') != 1:
            raise SystemExit('Pinned page layout changed; no extension prepared.')
        html = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', html)
        html = html.replace('</head>', '<link rel="stylesheet" href="pactlane.css" /></head>')
        files[name] = html.encode('utf-8')
    for name in ['icon-128.png', 'icon-34.png']:
        files[name] = (ROOT / 'packages/extension/src/assets/img' / name).read_bytes()
    for name in ['pactlane.css', 'manrope.woff2', 'OFL.pactlane.txt', 'pactlane-mark.svg']:
        if name in files:
            raise SystemExit('Unexpected presentation asset collision.')
        files[name] = (ROOT / 'pactlane/branding' / name).read_bytes()
    changed = {name for name in before if files[name] != before[name]}
    added = set(files) - set(before)
    if changed != {WORKER, 'manifest.json', 'content.styles.css', 'confirmPopup.html', 'options.html', 'icon-128.png', 'icon-34.png'} or added != {'pactlane.css', 'manrope.woff2', 'OFL.pactlane.txt', 'pactlane-mark.svg'}:
        raise SystemExit('Unexpected modified-file set; no extension prepared.')
    if any(old_manifest.get(key) != manifest.get(key)
           for key in set(old_manifest) | set(manifest) if key not in {'name', 'version_name', 'description'}):
        raise SystemExit('Unexpected manifest change; no extension prepared.')

    audit = {
        'baseRelease': VERSION,
        'originalSha256': ORIGINAL_SHA256,
        'versionName': VERSION_NAME,
        'upstreamRepository': 'https://github.com/tlsnotary/tlsn-extension',
        'upstreamCommit': UPSTREAM_COMMIT,
        'forkRepository': 'https://github.com/vmichalik/pactlane-tlsnotary',
        'packagingMethod': 'Checksum-verified upstream ZIP with the documented worker, manifest and presentation edits',
        'setupAndCryptographyTestedLive': False,
        'setupTimeoutMs': 60000,
        'changesApplyTo': ['direct MPC setup', 'relay setup'],
        'cryptographicRuntimeChanged': False,
        'permissionsChanged': False,
        'modifiedFiles': [],
        'addedFiles': [],
        'presentationOnlySincePactlane1': True,
        'unchangedFiles': [],
        'packageFile': PACKAGE,
    }
    for name in sorted(files):
        record = {'path': name, 'sha256': digest(files[name])}
        if name in added:
            audit['addedFiles'].append(record)
        elif name in changed:
            record['originalSha256'] = digest(before[name])
            audit['modifiedFiles'].append(record)
        else:
            audit['unchangedFiles'].append(record)

    source_paths = ['packages/extension/src/offscreen/ProveManager/worker.ts',
                    'packages/extension/src/manifest.json', 'pactlane/package.py',
                    'pactlane/INSTALL.md', 'pactlane/watchdog.test.mjs', 'LICENSE.pactlane']
    source_paths += ['packages/extension/src/entries/Content/content.styles.css', 'packages/extension/src/entries/ConfirmPopup/index.html', 'packages/extension/src/entries/Options/index.html', 'packages/extension/src/assets/img/icon-128.png', 'packages/extension/src/assets/img/icon-34.png', 'packages/extension/webpack.config.js']
    source_paths += ['pactlane/branding/' + name for name in ['pactlane.css', 'manrope.woff2', 'OFL.pactlane.txt', 'pactlane-mark.svg']]
    audit['sourceFiles'] = {name: digest((ROOT / name).read_bytes()) for name in source_paths}
    try:
        audit['sourceCommit'] = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        audit['sourceTreeDirty'] = bool(subprocess.check_output(
            ['git', 'status', '--porcelain'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip())
    except (OSError, subprocess.CalledProcessError):
        audit['sourceCommit'] = None
        audit['sourceTreeDirty'] = None
    install = (ROOT / 'pactlane/INSTALL.md').read_bytes()
    archive_files = {'Pactlane TLSNotary/extension/' + name: body for name, body in files.items()}
    archive_files['Pactlane TLSNotary/Install.md'] = install
    archive_files['Pactlane TLSNotary/LICENSE.pactlane'] = (ROOT / 'LICENSE.pactlane').read_bytes()
    archive_files['Pactlane TLSNotary/provenance.json'] = (json.dumps(audit, indent=2) + '\n').encode()

    output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.TemporaryDirectory(prefix='.' + output.name + '-prepare-', dir=output.parent) as temporary:
        staged = Path(temporary) / 'prepared'
        runtime = staged / 'extension'
        runtime.mkdir(parents=True, mode=0o700)
        for name, body in files.items():
            path = runtime / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        package_path = staged / PACKAGE
        with zipfile.ZipFile(package_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
            for name in sorted(archive_files):
                # Fixed timestamps and order make packages from one commit repeatable.
                entry = zipfile.ZipInfo(name, date_time=(2026, 10, 25, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                package.writestr(entry, archive_files[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        audit['packageSha256'] = digest(package_path.read_bytes())
        (staged / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
        (staged / 'SHA256SUMS').write_text(audit['packageSha256'] + '  ' + PACKAGE + '\n')
        (staged / 'Install.md').write_bytes(install)
        if output.exists():
            raise SystemExit('Output appeared during preparation; nothing was overwritten.')
        os.rename(staged, output)

    print(json.dumps({
        'output': str(output), 'extension': str(output / 'extension'),
        'package': str(output / PACKAGE), 'packageSha256': audit['packageSha256'],
        'modifiedFiles': sorted(changed), 'addedFiles': sorted(added), 'unchangedFiles': len(before) - len(changed),
        'installed': False, 'published': False,
    }))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path,
                        default=ROOT / 'downloads' / ('extension-' + VERSION + '.zip'),
                        help='Official upstream release ZIP; the packager does not download files')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist' / VERSION_NAME,
                        help='New output directory for the extension, ZIP and provenance')
    args = parser.parse_args()
    try:
        prepare(args.archive.expanduser().resolve(), args.output.expanduser().resolve())
    except (OSError, ValueError, UnicodeError, zipfile.BadZipFile):
        raise SystemExit('Unable to prepare the pinned release; check the archive, output and filesystem access.') from None


if __name__ == '__main__':
    main()
