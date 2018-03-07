#from gmusicapi import Mobileclient 
import pdb
import argparse

def parseTokens(api, tokenFile):
    playlistTokens = []
    f = open(tokenFile, 'r')
    for line in f:
        if '%3D' not in line:
            line = line.rstrip()
            playlistTokens.append(line)
        else:
            line.replace('%3D', '=')
            line = line.rstrip()
            playlistTokens.append(line)
    f.close()
    return playlistTokens

def parseNames(api, nameFile):
    playlistNames = []
    f = open(nameFile, 'r')
    if f:
        for line in f:
            line = line.rstrip()
            playlistNames.append(line)
            #pdb.set_trace()            
    f.close()
    return playlistNames

def getPlaylistsFromNames(api, nameList):
#gather all of the named playlists that match the provided name file
    totalPlaylists = api.get_all_playlists()
    validPlaylists = []
    for playlist in totalPlaylists: #remove deleted playlists (why are these still here?)
        if playlist['deleted']:
            totalPlaylists.remove(playlist)
    for name in nameList:
        for playlist in totalPlaylists:
            if name.lower() == playlist['name'].lower():
                validPlaylists.append(playlist)
    assert(validPlaylists)
    return validPlaylists
    
def getPlaylistsFromTokens(api, tokenList):
#gather all of the shared playlists by their tokens
    playlists = []
    playlist.append(destPlaylist)
    for token in tokenList:
        currPlaylist = api.get_shared_playlist_contents(token)
        if currPlaylist:
            playlists.append(currPlaylist)
    assert(len(playlists)>1)
    return playlists
    
def retrievePlaylistFromName(api, playlistName):
    userPlaylists = api.get_all_user_playlists()
    for playlist in userPlaylists:
        if playlistName.lower() == playlist['name']:
            return playlist['id']
    return None

def merge(api, destName, playlists):
    playlistIndex = 0
    trackIds = []
    currIds = []
    createdPlaylists = []
    destNameAsList = destName.split(destName)
    destPlaylist=getPlaylistsFromNames(api, destNameAsList)
    playlists.append(destPlaylist)
    
    for playlist in playlists:
        for track in playlist:
            if track["trackId"] not in trackIds: 
                trackIds.append(track["trackId"])

    for trackId, index in enumerate(trackIds):
        if not index % 1000 and trackId not in destPlaylist:
            currIds.append(trackId)
        else:
            api.add_songs_to_playlist(playlistId, currIds)
            del currIds[:]
            currIds.append(trackId)
            destName = destName+str(index/1000)
            playlistId = api.create_playlists(destName)
    
def main():
    parser = argparse.ArgumentParser()
    api = Mobileclient()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-tf", "--tokenFile", help="text file with one token on each line")
    group.add_argument("-nf", "--nameFile", help="text file with one playlist title on each line. NOTE: The playlists must be in your library")
    parser.add_argument("email", help="email to be used for login in order to fetch playlists")
    parser.add_argument("password", help="app-specific password associated with the provided email")
    parser.add_argument("dest_playlist_name", help="name of destination playlist")
    args = parser.parse_args()

    api.login(args.email, args.password, Mobileclient.FROM_MAC_ADDRESS)
    assert(api.is_authenticated())
        
    playlistId = retrievePlaylistFromName(args.dest_playlist_name)
    if not destPlaylist:
        playlistId = api.create_playlist(args.dest_playlist_name)
    
    if args.tokenFile:
        tokenList = parseTokens(api, args.tokenFile)
        playlists = getPlaylistsFromTokens(api, tokenList)
    elif args.nameFile:
        nameList = parseNames(api, args.nameFile)
        playlists = getPlaylistsFromNames(api, nameList)
            
    merge(api, args.dest_playlist_name, playlists)
    api.logout()


if __name__ == "__main__":
    main()

'''outrunLinks = ["AMaBXylIL3CQ_aZYzIpNzAi9LVcGHQ7tDmBIbVE8dVbDLU4J4V10kD1YT3DYE2xHDt6yKClx1qTx4YCuv7fHNU3lhyoOjSAQxw==",
        "AMaBXykt_DsUhDk_9Uyu0TsX8WLNSP9cLz9iJn2fUrOQlf01MWHpbq34q1-NLQecbobGBUUpLzvebSidqmuiQi4X2lDnHvFI_A==",
        "AMaBXynd_AxgjJrwumIFLf6VV6W2csWiEtU68YwB-GMn_8Hf9TbINhBD2THXxaVFDqYogjGJgHQajRsBN9Bb-JrCQ2u5TJG9yQ==", 
        "AMaBXymtOWAzQPfKlD8fSWI6UQEjsIyV_7kvQWPSrV7860ZGSxtJGQZ4KwyTsff7wnZW6GmGmP917lijIJ1nyl_LJ_2Jfy7P-w==", 
        "AMaBXynw-Jp1c85Yx6B5fScef-ySUdHUojbdivqAbQPH7aeqIS8TBLZ5jEMl9c1ss63xXAiAJo1clSCl2hrHDxljXa9KofcbGA==", 
        "AMaBXym2Tj8PtYlHEENwqUepJ6hTVAeAe4aBAQcqxc9EL2gaa_ZKsl7CzNwCnP0cOlYhLaa29sulfbpETYDY-0_KKcL0n0w=="]
'''