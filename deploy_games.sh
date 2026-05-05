#!/bin/bash
# deploy_games.sh — deploy birch and kuule from kaiku/games/ to rebraining.org
# Canonical source for both games is kaiku/games/. Run from the kaiku/ directory.
# These are demos and proofs of concept. Deliberately hostile. 13 minutes each.
# You play them for 13 minutes or you don't. Either way takes 13 minutes.

set -euo pipefail

BUCKET="eerikki.jamesmcgill.us"
DIST_ID="E1J43EN4RNCKX0"

GAMES="$(dirname "$0")/games"

echo "→ deploying games from $GAMES"

aws s3 cp "$GAMES/kuule.html" "s3://$BUCKET/kuule" --content-type "text/html; charset=utf-8"
aws s3 cp "$GAMES/birch.html" "s3://$BUCKET/birch" --content-type "text/html; charset=utf-8"

echo "→ files uploaded"

echo "→ invalidating /kuule and /birch"
aws cloudfront create-invalidation \
  --distribution-id "$DIST_ID" \
  --paths "/kuule" "/birch" \
  --query 'Invalidation.Id' \
  --output text
echo "→ invalidation submitted"

echo "→ done"
