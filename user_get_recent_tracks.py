import psycopg2
import psycopg2.extras
import urllib.request
import json

host_name = 
port_number = 
dbname = 
rolename = 
passwd = 

def main():
    call_url1 = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&limit=200&user="
    user_name = {YOUR_NAME}
    call_url2 = "&api_key="
    api_key = {YOUR_API_KEY}
    call_url3 = "&format=json"
    api_call_url = call_url1 + user_name + call_url2 + api_key + call_url3
    print(api_call_url)
    address_json = urllib.request.urlopen(api_call_url)
    data = json.loads(address_json.read())
    recenttracks = data["recenttracks"]
    track = recenttracks["track"]
    conn = psycopg2.connect(database=dbname, host=host_name, port=port_number, user=rolename, password=passwd)
    cur = conn.cursor()
    for i in range(200):
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
            track_data1 = (artist_infomation, song_infomation, album_infomation, time_stamp)
            track_data2 = (artist_infomation, song_infomation)
            cur.execute("""INSERT INTO track_data(artist, song, album, time_stamp)VALUES(%s, %s, %s, %s)""", track_data1)
            conn.commit()
            cur.execute("INSERT INTO ungot_similar_tracks(artist, track)VALUES(%s, %s)", track_data2)
            conn.commit()

        except KeyError:
            continue
        except psycopg2.IntegrityError:
            break
    conn.close()


if __name__ == '__main__':
    main()