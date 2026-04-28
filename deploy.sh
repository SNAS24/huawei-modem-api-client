docker build -t huawei-sms-reader .

docker run --rm \
  -e MODEM_IP="192.168.110.254" \
  -e MODEM_USER="admin" \
  -e MODEM_PASS="ваш_пароль" \
  huawei-sms-reader
