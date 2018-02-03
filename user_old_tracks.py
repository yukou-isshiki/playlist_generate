# -*- coding: utf-8 -*-
import urllib.request
import json
import sqlite3

def main():
    call_url1 = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&limit=200&user="
    user_name = {YOUR_NAME}
    call_url2 = "&page="
    page_number = "73"
    call_url3 = "&api_key="
    api_key = {YOUR_API_KEY}
    call_url4 = "&format=json"
    api_call_url = call_url1 + user_name + call_url2 + page_number + call_url3 + api_key + call_url4
    print(api_call_url)
    address_json = urllib.request.urlopen(api_call_url)
    data = json.loads(address_json.read())
    recenttracks = data["recenttracks"]
    track = recenttracks["track"]
    dbpath = {YOUR_DB}
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for i in range(12):
        try:
            track_infomation = track[i]
            artist_infomation = track_infomation["artist"]
            artist_infomation = artist_infomation["#text"]
            song_infomation = track_infomation["name"]
            album_infomation = track_infomation["album"]
            album_infomation = album_infomation["#text"]
            time_stamp = track_infomation["date"]
            time_stamp = time_stamp["#text"]
            print("アーティスト:{}".format(artist_infomation))
            print("曲:{}".format(song_infomation))
            print("収録アルバム:{}".format(album_infomation))
            print("聴取日時:{}".format(time_stamp))
            track_data = (artist_infomation, song_infomation, album_infomation, time_stamp)
            cur.execute("""INSERT INTO track_data(artist, song, album, time_stamp)VALUES(?, ?, ?, ?)""", track_data)
            conn.commit()

        except KeyError:
            continue
        except sqlite3.IntegrityError:
            continue
    cur = conn.cursor()
    cur.execute("SELECT artist, song, album, time_stamp FROM track_data")
    item_list = cur.fetchall()
    for it in item_list:
        print(it)
    conn.close()


if __name__ == '__main__':
    main()
