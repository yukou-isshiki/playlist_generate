# -*- coding: utf-8 -*-

import urllib.request
import json
import sqlite3

def main():
    dbpath = {YOUR_DB}
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute("SELECT artist, song FROM not_found_similar_track ORDER BY artist ASC")
    item_list = cur.fetchall()
    for it in item_list:
        artist = it[0]
        song = it[1]
        not_found_track_data = (artist, song)
        cur.execute(
            "SELECT * FROM similar WHERE from_artist = ? AND from_song = ?",
            not_found_track_data)
        similar_list = cur.fetchall()
        if similar_list == []:
            print(artist)
            print(song)
            artist = urllib.parse.quote(artist)
            song = urllib.parse.quote(song)
            api_call_url1 = "http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist="
            api_call_url2 = "&track="
            api_call_url3 = "&api_key="
            api_key = {YOUR_API_KEY}
            api_call_url4 = "&format=json"
            api_call_url = api_call_url1 + artist + api_call_url2 + song + api_call_url3 + api_key + api_call_url4
            try:
                address_json = urllib.request.urlopen(api_call_url)
                data = json.loads(address_json.read())
                similartracks = data["similartracks"]
                track = similartracks["track"]
                for i in range(100):
                    track_infomation = track[i]
                    song_infomation = track_infomation["name"]
                    match_index = track_infomation["match"]
                    artist_infomation = track_infomation["artist"]
                    artist_infomation = artist_infomation["name"]
                    artist = urllib.parse.unquote(artist)
                    song = urllib.parse.unquote(song)
                    similar_track_data = (artist, song, artist_infomation, song_infomation, match_index)
                    print(similar_track_data)
                    cur.execute(
                        "INSERT INTO similar(from_artist, from_song, to_artist, to_song, match_index)VALUES(?, ?, ?, ?, ?)",
                        similar_track_data)
                    cur.execute("DELETE from not_found_similar_track WHERE artist = ? AND song = ?",
                                    not_found_track_data)
                    conn.commit()
            except IndexError:
                continue
        else:
            cur.execute("DELETE from not_found_similar_track WHERE artist = ? AND song = ?", not_found_track_data)
            conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
