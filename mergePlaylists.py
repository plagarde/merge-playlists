from gmusicapi import Mobileclient 
import pdb
import argparse
parser = argparse.ArgumentParser()
api = Mobileclient()
email = raw_input("Please enter your email:") 
password = raw_input("Please enter your password: (app-specific if you have 2fa enabled)")
api.login(email, password, Mobileclient.FROM_MAC_ADDRESS)
#api.login(email, password, Mobileclient.FROM_MAC_ADDRESS)

outrunLinks = ["AMaBXylIL3CQ_aZYzIpNzAi9LVcGHQ7tDmBIbVE8dVbDLU4J4V10kD1YT3DYE2xHDt6yKClx1qTx4YCuv7fHNU3lhyoOjSAQxw==",
        "AMaBXykt_DsUhDk_9Uyu0TsX8WLNSP9cLz9iJn2fUrOQlf01MWHpbq34q1-NLQecbobGBUUpLzvebSidqmuiQi4X2lDnHvFI_A==",
        "AMaBXynd_AxgjJrwumIFLf6VV6W2csWiEtU68YwB-GMn_8Hf9TbINhBD2THXxaVFDqYogjGJgHQajRsBN9Bb-JrCQ2u5TJG9yQ==", 
        "AMaBXymtOWAzQPfKlD8fSWI6UQEjsIyV_7kvQWPSrV7860ZGSxtJGQZ4KwyTsff7wnZW6GmGmP917lijIJ1nyl_LJ_2Jfy7P-w==", 
        "AMaBXynw-Jp1c85Yx6B5fScef-ySUdHUojbdivqAbQPH7aeqIS8TBLZ5jEMl9c1ss63xXAiAJo1clSCl2hrHDxljXa9KofcbGA==", 
        "AMaBXym2Tj8PtYlHEENwqUepJ6hTVAeAe4aBAQcqxc9EL2gaa_ZKsl7CzNwCnP0cOlYhLaa29sulfbpETYDY-0_KKcL0n0w=="]

outrunPlaylists = []
for link in outrunLinks:
    outrunPlaylists.append(api.get_shared_playlist_contents(link))
myOutrunPlaylistList = []
myOutrunPlaylist=api.create_playlist("My outrun")
myOutrunPlaylist2=api.create_playlist("My second outrun")

#pdb.set_trace()
index = 0
for playlist in outrunPlaylists:
    for track in playlist:
        if track["trackId"] not in myOutrunPlaylist: 
            myOutrunPlaylistList.append(track["trackId"])
            index += 1
        
api.add_songs_to_playlist(myOutrunPlaylist, myOutrunPlaylistList[:999])

api.add_songs_to_playlist(myOutrunPlaylist2, myOutrunPlaylistList[1000:])
