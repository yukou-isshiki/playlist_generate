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
    conn = psycopg2.connect(database=dbname, host=host_name, port=port_number, user=rolename, password=passwd)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT to_artist FROM similar_track ORDER BY to_artist DESC")
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
                cur.execute("SELECT * FROM similar_artist WHERE from_artist = %s AND to_artist = %s AND match_index = %s", similar_artist_data)
                similar_artists_list = cur.fetchall()
                if similar_artists_list == []:
                    cur.execute("INSERT INTO similar_artist(from_artist, to_artist, match_index)VALUES(%s, %s, %s)", similar_artist_data)
                    conn.commit()
                    print(similar_artist_data)
        except:
            IndexError
            continue
    conn.close()




if __name__ == '__main__':
    main()
