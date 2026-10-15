# Gathering 28 image process

Mode: built-in `image_gen.imagegen`, edit with the downloaded and inspected
Gathering 27 wall as the sole reference image. No CLI fallback, external
runtime dependency, secret or environment lookup was used. The tool returned
actual 1254 × 1254 PNG bytes. The model's new sieve motif was used; the rest
of its edited background was discarded to preserve exact ancestral pixels.

Final generation prompt:

> Edit target: the supplied square prehistoric gathering cave wall. Keep its exact square dimensions, framing, rock texture, cracks, torchlight, colors, and EVERY existing pigment mark completely unchanged. Preserve the existing large Pepe the frog, his heavy lidded eyes and wide mouth and his two FIVE-digit hands (four fingers and one thumb each). Add only ONE small earth-pigment motif on the empty rock at normalized x=0.47, y=0.81 (below the woven bridge and left of the existing black ring): a little prehistoric woven SIEVE, a shallow ochre basket bowl with sparse charcoal crosshatching and three small ochre stones held inside it. This symbolizes bounded collection of useful evidence. It should occupy only about 7 percent of the wall width and 5 percent of height. Handmade, irregular, worn red/yellow ochre and charcoal strokes, bare rock showing through, same Lascaux/Chauvet cave painting style as ancestors. Do not add a new frog or any hands. No letters, numbers, captions, signatures, logos, watermark, border, frame, photography, 3D, real people, political or hateful symbols. Make a strictly additive edit, no erased, moved, redrawn or repainted ancestors.

The generated edit changed background pixels, so it was not accepted as a full
replacement. `finish_wall28.js` transferred only newly darker earth pigment
from the generated sieve region to empty lower rock, with a feathered mask.
It scaled the motif slightly to fit the empty rock. This leaves a deliberately
worn, faint mark. Original ancestor pixels everywhere outside the small addition
box are exact; every existing mark lies outside it. No generated ancestor
redraw was retained. The export compared all pixels and recorded 2,151 changed
pixels, zero outside the box. The generated PNG was overwritten by the final
wall, leaving only the requested wall and its continuation plus the JPEG.

Final paths: `artifacts/gathering/wall-v8.png`, continuation
`artifacts/gathering/wall.png`, and `dist/gathering/28.jpg`. Both final image
formats were opened in the viewer for explicit review; see VISUAL_REVIEW.md.
