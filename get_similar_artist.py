import urllib.request
import json
import sqlite3

def main():
    dbpath = {YOUR_DB}
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT to_artist FROM similar ORDER BY to_artist DESC")
    item_list = cur.fetchall()
    for it in item_list:
        artist = it[0]
        print(artist)
        artist = urllib.parse.quote(artist)
        url1 = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist="
        url2 = "&api_key="
        api_key = {YOUR_API_KEY}
        url3 = "&format=json"
        api_call_url = url1 + artist + url2 + api_key + url3
        print(api_call_url)
        try:
            address_json = urllib.request.urlopen(api_call_url)
            data = json.loads(address_json.read())
            similar_artists = data["similarartists"]
            artist_dict = similar_artists["artist"]
            for i in range(100):
                artist = urllib.parse.unquote(artist)
                artist_infomation = artist_dict[i]
                to_artist = artist_infomation["name"]
                match_index = artist_infomation["match"]
                similar_artist_data = (artist, to_artist, match_index)
                cur.execute("SELECT * FROM similar_artist WHERE from_artist = ? AND to_artist = ? AND match_index = ?", similar_artist_data)
                similar_artists_list = cur.fetchall()
                if similar_artists_list == []:
                    cur.execute("INSERT INTO similar_artist(from_artist, to_artist, match_index)VALUES(?, ?, ?)", similar_artist_data)
                    conn.commit()
                    print(similar_artist_data)
        except:
            IndexError
            continue
    conn.close()




if __name__ == '__main__':
    main()
