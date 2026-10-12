#!/usr/bin/env python3
"""Check package structure and syntax without executing skill workflows."""

from pathlib import Path
import re
import shutil
import subprocess
import sys

import yaml


def main():
    root = Path(__file__).resolve().parents[1]
    skills = sorted((root / 'skills').iterdir())
    errors = []
    bash = shutil.which('bash')
    python_count = bash_count = 0
    if not skills:
        errors.append('No skills found')
    for skill in skills:
        manifest = skill / 'SKILL.md'
        if not manifest.is_file():
            errors.append(f'{skill.name}: missing SKILL.md')
            continue
        match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)',
                         manifest.read_text(encoding='utf-8'), re.S)
        try:
            data = yaml.safe_load(match.group(1)) if match else None
            if not isinstance(data, dict):
                raise ValueError('missing or invalid YAML frontmatter')
            if data.get('name') != skill.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', skill.name):
                raise ValueError('name must match the skill directory in hyphen-case')
            description = data.get('description')
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError('description must contain 1 to 1024 characters')
        except (yaml.YAMLError, ValueError) as error:
            errors.append(f'{skill.name}: {error}')
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if any(part in ('.git', '.venv', '__pycache__') for part in relative.parts) or not path.is_file():
            continue
        if path.suffix == '.md':
            for link in re.findall(r'(?<!!)\[[^\]]+\]\(([^\s)]+)(?:\s+[^)]*)?\)', path.read_text(encoding='utf-8')):
                if re.match(r'^[a-zA-Z][\w+.-]*:|^#', link):
                    continue
                target = link.split('#')[0]
                if target and not (path.parent / target).exists():
                    errors.append(f'{relative}: missing linked file {target}')
        elif path.suffix == '.py':
            try:
                compile(path.read_bytes(), str(path), 'exec')
                python_count += 1
            except SyntaxError as error:
                errors.append(f'{relative}: {error}')
        elif path.suffix == '.sh' and bash:
            result = subprocess.run([bash, '-n', str(path)], capture_output=True, text=True)
            if result.returncode:
                errors.append(f'{relative}: {result.stderr.strip()}')
            else:
                bash_count += 1
    for error in errors:
        print(error, file=sys.stderr)
    if not bash:
        print('SKIP: Bash syntax checks; bash is unavailable')
    if errors:
        print(f'FAIL: {len(errors)} errors', file=sys.stderr)
        return 1
    print(f'PASS: {len(skills)} skills, local file links, {python_count} Python files, {bash_count} Bash files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
