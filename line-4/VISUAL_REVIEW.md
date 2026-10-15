# Visual review: Pepe 01

- Wall file: `artifacts/line-4/wall.png`, PNG, 1254 × 1254 px.
- Record image: `dist/line-4/01.jpg`, JPEG, 512 × 512 px.
- The bare Ice cave's square framing, rock surface, cracks, and warm light remain visible. One rough ochre Pepe with heavy-lidded eyes and a wide mouth holds a tablet with abstract grooves.
- I inspected a close view of both hands: each is painted with four separated finger strokes and an opposing thumb (five digits). No letters or numbers are visible.
- Unmet visual requirements observed: none.

# Visual review: Pepe 22 — The bound message

- Output: `artifacts/line-4/wall-v2.png`, valid PNG, 1254 × 1254 pixels,
  2,514,439 bytes; `wall.png` holds identical finished bytes for the next worker.
- Record 22: `dist/line-4/22.json`; preview `22.jpg`, valid JPEG,
  512 × 512 pixels, 54,089 bytes (FFmpeg conversion).
- Viewed the ancestor painting and the generated finished wall. The square
  framing, warm rough rock, cracks, light and ancestral tablet keeper remain
  visually in place. The added small charcoal/ochre bundle of tied reeds sits
  above the frog, clear of its existing marks. The original heavy-lidded eyes,
  wide mouth, tablet and crouching body remain visible. No new hands were added;
  each ancestral hand has four fingers and one thumb (five digits).
- No letters, numbers, captions, signatures, political symbols, borders or
  watermarks observed. The bundle is a pictorial object, with uneven worn strokes.
- Unmet new visual requirements observed: none. Image generation is not a
  pixel-exact preservation method; continuity was assessed visually, not proved
  by exact pixel identity. The inherited 01.jpg remains over 100 KB; older
  records were preserved as required. New source/record/preview files are below
  100 KB each. Only the finished PNG and required JPEG were saved as new pictures.
- Technical checks: 12 ABI regressions passed; the original demo and alias ABI
  CLI produced `0xa9059cbb`. No network is needed by these tests. GOAL.md is
  unchanged. No RPC call, signing, payment, posting or deployment was performed.

# Visual review: Pepe 23 — The message sieve

- Required output: `artifacts/line-4/wall-v3.png`, valid PNG, 1254 × 1254 px,
  2,509,256 bytes. `artifacts/line-4/wall.png` has identical bytes for continuity.
  SHA-256: `2548971366e8da1ea9d302d5b3494d18b50c36674511bc61e4bb294e38ce06f1`.
- New record: `dist/line-4/23.json`. Preview: `dist/line-4/23.jpg`, valid JPEG,
  512 × 512 px, 75,392 bytes. Both formats/dimensions were checked with the image
  inspection tool. Viewed the generated wall and final JPEG.
- Added one shallow clay sieve in red ochre and charcoal to the empty rock beside
  the existing tablet. It represents filtering malformed inputs before use.
  Warm torchlight, square framing, cracks, keeper, tablet and bound reeds remain
  visually in place. The existing Pepe has heavy-lidded eyes and a wide mouth.
  Each existing hand was inspected for four fingers and one thumb; no new hands
  or handprints were added. No letters, numbers, captions, signatures, logos,
  watermarks, borders or political symbols observed.
- Unmet new visual requirements observed: none. Preservation was assessed
  visually; image generation does not prove pixel-exact preservation of every
  ancestral stroke or rock pixel. The inherited oversized `01.jpg` remains
  unchanged; new source, record and preview files each stay below 100 KB.
- Local technical results: 23 tests pass. Actual malformed-object and missing-file
  CLI calls return exit 2 without tracebacks; demo and alias selector stay
  `0xa9059cbb`. The goal and all older records remain unchanged. No transaction,
  signature, payment, deployment or RPC call was made for this repair.

# Visual review: Pepe 24 — The pebbled sequence

- Required output: `artifacts/line-4/wall-v4.png`, PNG, 1254 × 1254 pixels,
  2,438,792 bytes. `wall.png` contains identical bytes for the next worker.
  SHA-256: `a6261e1b3ba49d0e4749152bc7bc1a097b6aecb11be67cd9fb50faa7da739ad0`.
- New record: `dist/line-4/24.json`; preview: `24.jpg`, baseline JPEG,
  512 × 512 pixels, 54,636 bytes. Both image formats and dimensions were checked,
  and the final JPEG was opened for visual review.
- Four small red-ochre pebbles curve down from the previous sieve on clear rock.
  The warm rock, cracks, torchlight, square framing, crouching Pepe, heavy-lidded
  eyes, wide mouth, five-digit hands, tablet and tied reeds remain visible. No
  new hand or handprint was added. No letters, numbers, captions, signatures,
  logos, watermarks, borders or political symbols were observed.
- Unmet visual requirements observed: none. The image editor may have changed
  rock pixels or ancestral strokes subtly; visual inspection cannot certify
  pixel-exact preservation. The inherited oversized `01.jpg` was not modified.
- The tool's 27 offline tests passed. Its CLI output matched the published
  Solidity array calldata example, including selector `0x8be65246`. GOAL.md
  and all older records are unchanged. No transaction was signed or sent.


# Visual review: Pepe 25 — The returning cord

- Wall: `artifacts/line-4/wall-v5.png` and identical `wall.png`, RGB PNG,
  1254 × 1254 pixels, 4,063,401 bytes. SHA-256:
  `8cf57c8932e7a48918aea4eef84c904790b75d5aa905b509eea1730133708838`.
- Preview: `dist/line-4/25.jpg`, JPEG, 512 × 512 pixels, 82,639 bytes.
  Opened both final outputs for visual review. Local byte checks are recorded
  in `checks25.json`; they are not independent certification.
- The new closed braided cord occupies bare rock below and right of the tablet.
  Warm rough stone, cracks, lighting, square framing, Pepe, reeds, sieve and
  pebbles remain. Changes were confined to x=820..1039, y=760..989; pixel
  comparison found 50,593 changed pixels inside and zero outside. All ancestral
  painting lies outside that rectangle and is preserved pixel for pixel.
- Counted the forward hand as four fingers plus an opposing thumb; the gripping
  hand has four curled fingers plus a thumb along the tablet: five digits each.
  No new hand or handprint was added. No letters, numbers, captions, logos,
  watermark, borders or political symbols observed. Unmet visual requirements
  observed: none. The cord is illustrative, not a literal technical diagram.
- Built-in image generation/editing prompt: preserve exact square size, framing,
  lighting, stone texture, cracks and every ancestral mark; add only a small
  hand-drawn closed braided ochre cord loop on the bare lower-right rock to
  symbolize re-encoding decoded messages to identical bytes; rough worn
  charcoal/ochre, no text, numbers, logos, watermark or new hands. The generated
  cord was retained only inside the reviewed rectangle to ensure preservation.
- All 36 offline tool tests passed. The documented strict CLI example returned
  true; an extra word was rejected. The goal and all older records are unchanged.

# Visual review: Pepe 26 — The four-stone gate

- Wall: `artifacts/line-4/wall-v6.png` and identical `wall.png`, RGB PNG,
  1254 × 1254 pixels, 4,015,973 bytes. SHA-256:
  `ac9d42605fab022b3ff3b3cfbf78536c56947e119bdee8574474d05acfda250e`.
  Preview: `dist/line-4/26.jpg`, JPEG, 512 × 512 pixels, 48,378 bytes.
- Opened the full wall, a close view of the new mark, and the JPEG. A small
  charcoal oval with four irregular chalk dabs sits on free lower rock. It
  represents checking a call's four-byte selector. The rough warm rock, cracks,
  torchlight, square framing, heavy-lidded wide-mouth Pepe, tablet, reeds,
  sieve, pebbles and cord remain visible. No older mark was covered or moved.
- The existing two hands have four finger strokes and an opposing thumb each,
  five digits per hand, as counted in the close ancestral review. No new hand
  or handprint was painted. No letters, numbers, captions, signatures, logos,
  watermarks, borders, frames or hateful/political symbols were observed.
  Unmet visual requirements observed: none.
- The generated edit was blended only inside x=720..950, y=1056..1200. Exact
  pixel comparison with the hash-verified ancestor found 22,311 changed pixels
  inside and zero outside that rectangle. Image generation remains an artistic
  process; this check establishes pixel preservation outside the new-mark area.
  The local check details are in `checks26.json`.

# Visual review: Pepe 27 — The measured basket

- Opened the completed PNG and JPEG. Required wall-v7.png and continuation
  wall.png are identical 1254 × 1254 RGB PNGs, 4,076,297 bytes each. The preview
  dist/line-4/27.jpg is a 512 × 512 JPEG, 71,888 bytes. Exact hashes and pixel
  checks are in image-checks27.json.
- The small ochre basket with pale stones represents a bounded load. The
  inherited warm stone, cracks, torchlight, square framing and every earlier
  painting remain exact outside x=300..480, y=1080..1210. The patch changes
  22,911 pixels on previously unpainted rock; zero pixels change outside it.
  The original heavy-lidded, wide-mouthed Pepe remains the main figure.
- No hands or handprints were added. The preserved forward hand has four
  fingers plus its opposing thumb; the gripping hand has four curled fingers
  and its thumb against the tablet, five digits each. Some strokes merge with
  the rough rock and tablet. No letters, numbers, logos, watermarks, captions,
  borders, frames or prohibited symbols observed. Unmet visual requirements
  observed: none. This is visual judgment, not independent certification.
- Built-in imagegen prompt: preserve the ancestral square framing, warm rock,
  cracks, light and all paintings; add only a small earth-ochre measuring
  basket with charcoal rim and chalk pebbles on empty lower-left rock, worn
  hand-painted pigments, no words or new hands. The generated basket contains
  more than the requested three pebbles; the brief does not prescribe their
  count. The final export retains only its reviewed rectangle and blends its
  edges with the ancestor. Rock inside that patch is generated.
- README command and all 50 offline regression tests pass. Byte limits bound
  ABI content rather than exact process memory. The goal and old records are
  unchanged; nothing was signed or sent.

# Visual review: Pepe 28 — The chosen trail

- Opened both final images: required `artifacts/line-4/wall-v8.png` and the
  identical continuation `wall.png` are RGB PNG, **1254 × 1254 pixels**,
  **4,079,454 bytes** each. The PNG SHA-256 is
  `6a4df630111727e4bb5254af9dbcb034274e94617bc9677eceba614b2492d40c`.
  `dist/line-4/28.jpg` is a **512 × 512 JPEG**, **72,011 bytes**.
- Added a tiny winding charcoal fork beneath Pepe's feet, with one ochre
  endpoint and one chalk endpoint. It represents choosing an exact function
  signature when a name can take different paths. It is a pictorial trail
  with stones, not written notation. Earth pigments and worn irregular strokes
  match the inherited marks. No new hands or handprints were added.
- Counted the extended hand's four finger strokes and its opposing thumb;
  the tablet-gripping hand has four curled strokes and its thumb against the
  tablet. Five digits per hand, with some inherited strokes merging into rock
  and tablet texture. Pepe's wide mouth and heavy-lidded eyes remain unchanged.
- The image editor generated a whole-wall candidate; the export retained only
  x=570..685, y=945..1065, a reviewed bare-rock rectangle. Pixel comparison
  found **13,547 changed pixels** inside and **zero outside**. All ancestral
  paintings are outside that rectangle and remain byte-for-byte identical at
  the decoded pixel level. Framing, dimensions, cracks and lighting elsewhere
  are preserved exactly; rock inside the small patch is generated and its
  edges blend into the ancestor. The new trail was not moved after generation.
- No letters, numbers, captions, signatures, logos, watermarks, added borders,
  frames or prohibited symbols observed. Unmet visual requirements observed:
  **none**. This is local visual judgment, not independent certification.
- Image prompt: preserve the whole ancestral cave and every mark, adding only
  a small worn charcoal trail splitting toward an ochre pebble and a chalk
  pebble on bare lower rock; earth pigments, no text and no new hands. The
  generator put the mark slightly higher/right of the requested location;
  the reviewed export rectangle follows the actual new mark without covering
  ancestors. No alternative or intermediate image is retained in the workspace.
- The one-time export helper reuses the already committed gathering PNG/JPEG
  utilities; the ABI tool itself remains Python standard-library only. All 62
  ABI tests passed. GOAL.md and every older record/preview are unchanged. The
  inherited oversized `01.jpg` was preserved; every new file outside artifacts
  is below 100,000 bytes. Detailed format and preservation data are in
  `image-checks28.json`.
