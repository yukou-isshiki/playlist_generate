import sqlite3

def get_artist_similar():
    dbpath = {YOUR_DB}
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute("SELECT to_artist FROM similar_artist WHERE from_artist = ? AND match_index > 0.01 ORDER BY match_index DESC", (artist,))
    similar_artist_list = cur.fetchall()
    conn.close()
    return similar_artist_list

def get_most_similar_song():
    dbpath = {YOUR_DB}
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    similar_artist_list = get_artist_similar()
    playlist = []
    playlist.append(first_input)
    if similar_artist_list == []:
        print("類似するアーティストが登録されていないか、打ち間違いの可能性があります。")
    else:
        cur.execute("SELECT to_artist, to_song FROM similar WHERE from_artist = ? AND from_song = ? AND match_index = 1.0", first_input)
        similar_tracklist = cur.fetchall()
        if similar_tracklist == []:
            cur.execute("SELECT from_artist, from_song FROM similar WHERE from_artist = ?", (artist, ))
            similar_tracklist = cur.fetchall()
            similar_track = similar_tracklist[0]
            playlist.append(similar_track)
            return playlist
        else:
            similar_track = similar_tracklist[0]
            playlist.append(similar_track)
            return playlist
    conn.close()

def generate_playlist():
    dbpath = {YOUR_DB}
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    similar_artist_list = get_artist_similar()
    playlist = get_most_similar_song()
    for i in range(len(similar_artist_list) - 1):
        if len(playlist) == 15:
            return playlist
        else:
            similar_artist = similar_artist_list[i]
            search_word = (first_input[0], first_input[1], similar_artist[0])
            cur.execute("SELECT to_artist, to_song FROM similar WHERE from_artist = ? AND from_song = ? AND to_artist = ? AND match_index > 0.01 ORDER BY match_index DESC", search_word)
            similar_tracklist = cur.fetchall()
            for j in range(len(similar_tracklist) - 1):
                trackdata = similar_tracklist[j]
                if trackdata in playlist:
                    continue
                else:
                    playlist.append(trackdata)
    conn.close()

def playlist_print():
    playlist = generate_playlist()
    print(playlist)

if __name__ == '__main__':
    artist = input("検索したいアーティスト名を入力して下さい")
    song = input("次にアーティストの楽曲名を入力して下さい")
    first_input = (artist, song)
    playlist_print()

