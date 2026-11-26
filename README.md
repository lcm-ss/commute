# 上下班路況連結

一個放在 GitHub Pages 的簡單網頁,點開就能看路況。不需要 API Key、不需要 Secrets。

## 啟用步驟
1. 把 `index.html` 放到 repo 根目錄並 push。
2. Repo → **Settings → Pages** → Source 選 **Deploy from a branch** → Branch 選 `main`、資料夾 `/ (root)` → Save。
3. 約 1 分鐘後網址為:`https://<你的帳號>.github.io/<repo名稱>/`
4. 手機瀏覽器開啟後「加入主畫面」,就像 App 一樣一鍵點開。

## 使用
- 第一次開啟,展開「設定地址」填家、公司、交通方式,儲存即可(只存在你的瀏覽器)。
- 中午前自動把「上班路況」放在最上面,中午後則是「下班路況」。
- 也可以用網址參數直接帶入:
  `.../?home=台中車站&work=台中市政府&mode=two-wheeler`
  (`mode` 可用 `driving`、`two-wheeler`、`transit`、`walking`)
- 按鈕會開啟 Google 地圖導航頁,顯示目前即時路況與預估時間。
