"""
Get listing-ids via GET to https://www.fab.com/i/listings/search?currency=USD&seller=Quixel&sort_by=listingTypeWeight&cursor=bz03Njg%3D
where cursor is given by previoud search, cursors.next/previous

This is in div with id="js-dom-data-prefetched-data"
Looking for listing-id dc4dc139-f3a3-4375-875f-d1831506953e
prop licenses, array, find license with "name": "Professional" or "slug": "professional", and get its "offerId": "995b4f8437f4493bba976231b99f958b",

Then make post to https://www.fab.com/i/listings/a984aac1-d20f-4232-8ce8-212e1695aaf6/add-to-library
With Cookie, Referer, X-CsrfToken Header
and body form-data with offer_id=the_id
"""

import requests, json, os
import cloudscraper
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

scraper = cloudscraper.create_scraper()

# PARAMS to execute batch of requests.
# If either below is set to False but json files do not exist, searches will be performed anyway
# Perform search of that seller for its listings
perform_search = False
# Perform request to get offerId for each listing
perform_offerid_requests = False

# Quixel Search URL
# Open a session on fab.com, then go to a listing and look for csrf_token, session_id in the request COOKIE header
# 環境変数からCSRFトークンとセッションIDを取得
csrf_token = os.getenv("CSRF_TOKEN")
session_id = os.getenv("SESSION_ID")
seller = "Quixel"
max_searches = 1000  # 最大検索回数


##
# SEARCH LISTINGS FOR A GIVEN SELLER OR LOAD FROM FILE
##
def get_seller_listings(seller):
    search_url = f"https://www.fab.com/i/listings/search?seller={seller}&currency=USD&sort_by=listingTypeWeight"
    listings_fn = f"listings_seller_{seller}_max-searches_1000.json"
    if perform_search or not os.path.exists(listings_fn):
        results = []
        n_search = 1
        response = requests.get(search_url)
        if response.ok:
            data = response.json()
            # print(data)
            while (
                data["cursors"] and data["cursors"]["next"] and n_search < max_searches
            ):
                n_search += 1
                print(f"performing search #{n_search}")
                results.extend(data["results"])
                next_search_url = f'{search_url}&cursor={data["cursors"]["next"]}'
                response = requests.get(next_search_url)
                if response.status_code == 200:
                    data = response.json()
                else:
                    print("data status code is not 200")
                    break

        print(
            f"{len(results)} found after {n_search} searches out of max {max_searches}"
        )

        # print(json.dumps(listings_extract, indent=2))
        with open(
            f"listings_seller_{seller}_max-searches_{max_searches}.json",
            "w",
            encoding="utf8",
        ) as json_file:
            json.dump(results, json_file, ensure_ascii=True)
    else:
        # Importing a JSON file
        with open(listings_fn, "r") as file:
            results = json.load(file)
        print(f"imported {len(results)} listings from file {listings_fn}")

    return results


# GET OFFER ID VIA API REQUEST
def get_offer_id(listing_id):
    offer_id = None
    url = f"https://www.fab.com/i/listings/{listing_id}"
    response = scraper.get(url)
    if response.ok:
        data = response.json()
        licenses = data.get("licenses", [])
        pro_license = next((x for x in licenses if x.get("slug") == "professional"), None)
        if pro_license:
            offer_id = pro_license.get("offerId")
    return offer_id


##
## Attempt at making an offer to Add the listing to the user library
##
def add_to_library(listing_id, offer_id_pro, csrf_token, session_id):
    listing_url = f"https://www.fab.com/listings/{listing_id}"
    url = f"{listing_url.replace('fab.com', 'fab.com/i')}/add-to-library"
    headers = {
        "Cookie": f"sb_csrftoken={csrf_token}; sb_sessionid={session_id}",
        "Referer": listing_url,
        "X-CsrfToken": csrf_token,
    }
    resp = scraper.post(url, headers=headers, files={"offer_id": (None, offer_id_pro)})

    if resp.ok:
        print(f"Success: Added listing {listing_id} to library.")
    else:
        print(f"Failed to add listing {listing_id}, status: {resp.status_code}")
        print("Response text:", resp.text)  # エラーメッセージの出力

    return resp


##
# ADD TO LIBRRY FOR EVERY LISTTING OF INPUT results ARRAY
##
def add_all_listings_to_library(results):

    listings_fn = "listings_offerIds.json"
    if perform_offerid_requests or not os.path.exists(listings_fn):
        listings = [{"listing_id": r["uid"], "title": r["title"]} for r in results]
    else:
        with open(listings_fn, "r") as file:
            listings = json.load(file)
        print(f"imported {len(listings)} listings and offerIds from file {listings_fn}")

    listings_added = []
    listings_failed = []
    for idx, listing in enumerate(listings):
        print(f"{idx + 1}/{len(listings)}", end=" ")
        listing_id = listing["listing_id"]
        # if offerId exists, get it, otherwise, retrieve it via GET request
        if "offer_id" in listing:
            offer_id = listing["offer_id"]
        else:
            offer_id = get_offer_id(listing_id)
            listing["offer_id"] = offer_id
        resp = add_to_library(listing_id, offer_id, csrf_token, session_id)
        if resp.ok:
            print(f"success adding listing to library | {listing['title']}")
            listings_added.append(listing_id)
        else:
            print(
                f"FAILED with listingId: {listing_id}, offerId:{offer_id}, title: {listing['title']}"
            )
            listings_failed.append(listing_id)

        # Dump every 100 results and at the end
        if (idx % 10 == 0) or (idx == len(listings) - 1):
            with open(
                f"added_to_library_results.json",
                "w",
                encoding="utf8",
            ) as json_file:
                json.dump(
                    {
                        "n_listings_failed": len(listings_failed),
                        "n_listings_added": len(listings_added),
                        "listings_failed_ids": listings_failed,
                        "listings_added_ids": listings_added,
                        "listings_extract": listings,
                    },
                    json_file,
                    ensure_ascii=True,
                )
    print("done trying to add all listings to library, also wroting results to file")
    print(
        f"{len(listings_added)} added and {len(listings_failed)} failed out of {len(results)} total"
    )
    with open(
        listings_fn,
        "w",
        encoding="utf8",
    ) as json_file:
        json.dump(
            listings,
            json_file,
            ensure_ascii=True,
        )


# print([results[idx]["uid"] for idx in [8, 560, 612, 672, 674, 734, 1473]])
# FAILS Listing ids: ['6426cc8a-2410-45be-b3ce-edfea87d09cc', '6ceb57e8-ba46-4d5b-8010-0fb43084bc7b', '54720a35-daa0-4860-97be-67badb43c739', '64df9b4c-8412-4dec-b0b5-0876f92b3c45', 'a4244a40-3983-473a-bf0d-3538e15c02a6', 'a4244a40-3983-473a-bf0d-3538e15c02a6', '1db40ed0-bc01-41e2-bc05-830257b478a3', "9943cd49-36d7-4d74-92f5-5e70e9719f0d", "da896be1-9e7e-4b21-b90a-a5b4c492df9a", "da9190e9-43a5-4823-95b9-e11a44878206", "0c9760c2-dedd-48d9-a494-4bd581861364", "b5754cfa-fd34-41f0-a0e7-0e479cf80e04", "c8921002-a0d0-4e8d-ad89-5e0b23de0301", "d808f867-2560-4476-ad05-a1d999bd940b", "b097f354-640a-4f99-8a7e-e1e78eb8fd71", "f0f9cd8b-feb5-44b8-bc66-7f5c3151d19d", "9faf9fcc-2354-4f27-901b-78c490353620", "0217aeea-f1bd-40b6-a898-aad257b68de9", "e0b570b6-85b4-4f16-a1fb-cffd0c7a000a", "248b3817-9f4d-4bd0-ac6a-f41cea0cd8c2"]
# Fails after: look at failed.json on pc-reunion or command line terminal copy-paste and look for FAILED

results = get_seller_listings(seller)
# print(json.dumps(listings_extract[:3], indent=2))

add_all_listings_to_library(results)
