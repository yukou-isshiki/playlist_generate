# -*- coding: utf-8 -*-

import urllib.request
import json
import sqlite3

def main():
    dbpath = {YOUR_DB}
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    '''cur.execute("SELECT DISTINCT artist, track FROM ungot_similar_tracks ORDER BY artist DESC, track DESC")'''
    cur.execute("SELECT DISTINCT to_artist, to_song FROM similar ORDER BY to_artist DESC, to_song ASC")
    item_list = cur.fetchall()
    for it in item_list:
        artist = it[0]
        song = it[1]
        got_similar_track_data = (artist, song)
        cur.execute(
            "SELECT * FROM similar WHERE from_artist = ? AND from_song = ?",
            got_similar_track_data)
        similar_list = cur.fetchall()
        if similar_list == []:
            cur.execute("SELECT * FROM not_found_similar_track WHERE artist = ? AND song = ?", got_similar_track_data)
            not_similar_list = cur.fetchall()
            if not_similar_list == []:
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
                print(api_call_url)
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
                        conn.commit()
                        cur.execute("DELETE from ungot_similar_tracks WHERE artist = ? AND track = ?",
                                    got_similar_track_data)
                        conn.commit()
                except IndexError:
                    artist = urllib.parse.unquote(artist)
                    song = urllib.parse.unquote(song)
                    not_found_tracks = (artist, song)
                    cur.execute("INSERT INTO not_found_similar_track(artist, song)VALUES(?, ?)", not_found_tracks)
                    conn.commit()
                    print("該当トラックの情報がありませんでした")
                    cur.execute("DELETE from ungot_similar_tracks WHERE artist = ? AND track = ?",
                                got_similar_track_data)
                    conn.commit()
                    continue
                except KeyError:
                    f = open("not_found_tracks.txt", "a")
                    f.write("アーティスト:" + artist)
                    f.write("\r")
                    f.write("曲名:" + song)
                    f.write("\r")
                    f.close()
                    cur.execute("DELETE from ungot_similar_tracks WHERE artist = ? AND track = ?",
                                got_similar_track_data)
                    conn.commit()
                    continue
                except OSError:
                    print("pass")
                    continue
                except urllib.error.URLError:
                    print("pass")
                    continue
            else:
                cur.execute("DELETE from ungot_similar_tracks WHERE artist = ? AND track = ?",
                            got_similar_track_data)
                conn.commit()
                print("該当トラックの情報がありませんでした")
        else:
            cur.execute("DELETE from ungot_similar_tracks WHERE artist = ? AND track = ?",
                        got_similar_track_data)
            conn.commit()
            print("情報取得済み")
    conn.close()


if __name__ == '__main__':
    main()
