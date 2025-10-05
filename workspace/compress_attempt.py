from pathlib import Path
from PIL import Image
import hashlib

orig = Path(r"d:\IITM-1\workspace\download.png")
if not orig.exists():
    print("ERROR: original file not found:", orig)
    raise SystemExit(1)

def pixel_hash(img: Image.Image) -> str:
    # convert to a canonical mode for pixel comparison
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return hashlib.md5(img.tobytes()).hexdigest()

print('Original file:', orig)
print('Size bytes:', orig.stat().st_size)
with Image.open(orig) as im:
    print('Format:', im.format)
    print('Mode:', im.mode)
    print('Size:', im.size)
    orig_hash = pixel_hash(im)
    print('Pixel MD5:', orig_hash)

candidates = []
# Candidate 1: optimized PNG
out1 = orig.with_name('download_opt.png')
with Image.open(orig) as im:
    im.save(out1, format='PNG', optimize=True, compress_level=9)

candidates.append(out1)

# Candidate 2: lossless WebP
out2 = orig.with_name('download_lossless.webp')
with Image.open(orig) as im:
    im.save(out2, format='WEBP', lossless=True)

candidates.append(out2)

# Candidate 3: PNG via Pillow with palette won't be lossless (skip)

# Check candidates
for c in candidates:
    s = c.stat().st_size if c.exists() else None
    print('\nCandidate:', c)
    print('Size bytes:', s)
    try:
        with Image.open(c) as im2:
            h = pixel_hash(im2)
            print('Pixel MD5:', h)
            equal = (h == orig_hash) and (im2.size == Image.open(orig).size)
            print('Pixels identical to original?', equal)
    except Exception as e:
        print('Error opening candidate:', e)

# Print final success if any candidate meets criteria (<400 bytes and identical)
success = None
for c in candidates:
    if c.exists() and c.stat().st_size < 400:
        try:
            with Image.open(c) as im2:
                if pixel_hash(im2) == orig_hash and im2.size == Image.open(orig).size:
                    success = c
                    break
        except Exception:
            pass

if success:
    print('\nSUCCESS: produced lossless file under 400 bytes ->', success)
else:
    print('\nNo candidate met the <400 bytes lossless requirement.')
    print('You can inspect the generated files in the workspace:')
    for c in candidates:
        print(' -', c, 'size=', c.stat().st_size if c.exists() else 'missing')
