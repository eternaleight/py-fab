
[日本語](#fab-apicloudflareバイパス)

[English](#fab-api-bypass-cloudflare)


# fab-api（Cloudflareバイパス）

**元のコード参照:** [GitHub Gist - fab-api.py](https://gist.github.com/jo-chemla/b673d4a074562a794f4cda72437b4759) 
### Cloudflare回避機能を追加して正常に動作するように修正

※これは[fab-api.py](https://gist.github.com/jo-chemla/b673d4a074562a794f4cda72437b4759)を修正して正常に動作するようにしたものです。

| ![CleanShot 2024-10-29 at 00 47 34](https://github.com/user-attachments/assets/9aec1117-20fa-4180-9154-434947180573) |
|:--:|
| ライブラリに追加された状態 |

スクレイピングツールにCloudflare回避機能を追加しました。`cloudscraper`ライブラリを利用することで、Cloudflareの保護メカニズムを回避し、リクエストの成功を確保しています。

```python
import cloudscraper
scraper = cloudscraper.create_scraper()
```

リポジトリのダウンロード
```bash
git clone https://github.com/eternaleight/py-fab
```

1. 環境変数の設定 (.envファイル)

![CleanShot 2024-10-29 at 02 49 16green@2x](https://github.com/user-attachments/assets/bffa46e8-1bff-4bd6-baea-daeaf2266a37)

右クリック 検証 -> アプリケーション -> Cookie 
\
CSRF_TOKEN=xxxx <- sb_csrftokenこの値を入れる 
\
SESSION_ID=xxxx <- sb_sessionidこの値を入れる

```env
# .env
CSRF_TOKEN=YOUR_CSRF_TOKEN_HERE
SESSION_ID=YOUR_SESSION_ID_HERE
SELLER=Quixel
```

2. スクリプトの実行
```bash
python fab-api.py
```

| ![CleanShot 2024-10-29 at 00 25 06](https://github.com/user-attachments/assets/29d0f1f3-4740-4832-b2e6-399b396db5fd) |
|:--:|
| **Before:** リクエストに失敗 |

| ![CleanShot 2024-10-29 at 00 21 31](https://github.com/user-attachments/assets/b73d8dd2-9ae3-4a43-976f-76fa429e32fa) |
|:--:|
| **After:** リクエスト成功 ✅ |

# fab-api (Bypass Cloudflare)


**Original Code Reference:** [GitHub Gist - fab-api.py](https://gist.github.com/jo-chemla/b673d4a074562a794f4cda72437b4759)
### Added Cloudflare workaround and fixed it to work correctly


※This is a modification of the [fab-api.py](https://gist.github.com/jo-chemla/b673d4a074562a794f4cda72437b4759) so that it works correctly.


| ![CleanShot 2024-10-29 at 00 47 34](https://github.com/user-attachments/assets/9aec1117-20fa-4180-9154-434947180573) |
|:--:|
| Added to the library |

A Cloudflare bypass feature was implemented to allow the scraping tool to work effectively. The addition of the `cloudscraper` library resolves issues with Cloudflare's protection mechanisms, ensuring successful requests.

```python
import cloudscraper
scraper = cloudscraper.create_scraper()
```
Repository download

```bash
git clone https://github.com/eternaleight/py-fab
```

1. Set up environment variables (.env)

![CleanShot 2024-10-29 at 02 49 16green@2x](https://github.com/user-attachments/assets/bffa46e8-1bff-4bd6-baea-daeaf2266a37)


```env
# .env
CSRF_TOKEN=YOUR_CSRF_TOKEN_HERE
SESSION_ID=YOUR_SESSION_ID_HERE
SELLER=Quixel
```

2. Run the script
```bash
python fab-api.py
```

| ![CleanShot 2024-10-29 at 00 25 06](https://github.com/user-attachments/assets/29d0f1f3-4740-4832-b2e6-399b396db5fd) |
|:--:|
| **Before:** Request FAILED |

| ![CleanShot 2024-10-29 at 00 21 31](https://github.com/user-attachments/assets/b73d8dd2-9ae3-4a43-976f-76fa429e32fa) |
|:--:|
| **After:** Request SUCCESS ✅ |



