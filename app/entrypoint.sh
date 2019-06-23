#!/bin/sh

cat > config.json <<EOF
{
  "telegram_token": "$TELEGRAM_TOKEN",
  "authorized_chat_ids": $AUTHORIZED_CHAT_IDS
}
EOF

exec "$@"
