
## 功能
1. 使用容器開發、測試與佈署 FastApi APP
2. 開發與測試階段需要暫時 https 網址
3. 自動設定 ssl 的 nginx container
4. 開發完成後可以使用一個指令佈署完成


### 準備開發測試環境
1. docker-compose -f dev-docker-compose.yml up -d
2. 瀏覽器開啟: localhost:4040 取得暫時的 https 網址
3. 開始訪問暫時的網址測試服務

### 部署至prod
1. 開機器，取得 static ip，允許 http, https 流量，設定 ssh，安裝 docker, docker-compose
2. 設定 DNS 到 static ip
3. 將 domain name 填入 `prod-docker-compose.yml` 中的 frontend.environment.FQDN 中
4. docker-compose -f prod-docker-compose.yml up -d
5. 觀察服務啟動情況: docker-compose -f prod-docker-compose.yml logs -f
6. 開始訪問 domain name
