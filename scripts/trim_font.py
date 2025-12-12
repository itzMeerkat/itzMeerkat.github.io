import os
import glob
import subprocess

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', '_posts')
FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'raw_fonts')
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts')

# 1. Collect all unique characters from markdown files
def collect_characters(posts_dir, about_path, config_path):
    chars = set()
    # Collect from posts
    for md_file in glob.glob(os.path.join(posts_dir, '*.md')):
        with open(md_file, 'r', encoding='utf-8') as f:
            print(md_file)
            for line in f:
                chars.update(line.strip())

    # Collect from about.md
    with open(about_path, 'r', encoding='utf-8') as f:
        print(about_path)
        for line in f:
            chars.update(line.strip())

    with open(config_path, 'r', encoding='utf-8') as f:
        print(config_path)
        for line in f:
            chars.update(line.strip())

    chars.discard('\n')
    chars.discard('\r')
    return ''.join(sorted(chars))

# 2. Subset each font using pyftsubset
def subset_fonts(fonts_dir, charset):
    for font_file in os.listdir(fonts_dir):
        if font_file.lower().endswith('.ttf'):
            font_path = os.path.join(fonts_dir, font_file)
            output_path = os.path.join(OUT_DIR, font_file.replace('.ttf', '-subset.ttf'))
            print(f'Subsetting {font_file}...')
            cmd = [
                'pyftsubset',
                font_path,
                f'--output-file={output_path}',
                f'--text={charset}',
                # '--flavor=truetype',
                '--layout-features=*',
                '--glyph-names',
                '--symbol-cmap',
                '--legacy-cmap',
                '--notdef-glyph',
                '--notdef-outline',
                '--recommended-glyphs',
                '--name-IDs=*',
                '--name-legacy',
                '--drop-tables=',
            ]
            subprocess.run(cmd, check=True)
            print(f'Created {output_path}')

def main():
    print('Collecting characters from posts and about.md...')
    about_path = os.path.join(os.path.dirname(__file__), '..', 'about.md')
    config_path = os.path.join(os.path.dirname(__file__), '..', '_config.yml')
    charset = collect_characters(POSTS_DIR, about_path, config_path)
    print(f'Found {len(charset)} unique characters.')
    print(charset)
    print('Subsetting fonts...')
    subset_fonts(FONTS_DIR, charset)
    print('Done.')

if __name__ == '__main__':
    main()
