
import asyncio
import json
from fastmcp import Client

async def mcp_complex_queries():
    print("Chinook MCP Complex Queries Demo")
    print("===============================\n")
    
    # Connect to the MCP server
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        # Example 1: Find all tracks by AC/DC
        print("Example 1: Find all tracks by AC/DC (Artist ID 1)")
        print("------------------------------------------------")
        
        # Step 1: Get AC/DC's artist info
        result = await client.call_tool("get_record", {"table_name": "Artist", "record_id": 1})
        artist = json.loads(result[0].text)
        print(f"Artist: {json.dumps(artist, indent=2)}")
        
        # Step 2: Get all albums by AC/DC
        result = await client.call_tool("get_all_records", {"table_name": "Album", "limit": 100})
        all_albums = json.loads(result[0].text)
        ac_dc_albums = [album for album in all_albums if album['ArtistId'] == 1]
        print(f"Found {len(ac_dc_albums)} albums by AC/DC")
        
        # Step 3: Get all tracks from those albums
        all_tracks = []
        for album in ac_dc_albums:
            result = await client.call_tool("get_all_records", {"table_name": "Track", "limit": 100})
            tracks = json.loads(result[0].text)
            album_tracks = [track for track in tracks if track['AlbumId'] == album['AlbumId']]
            all_tracks.extend(album_tracks)
        
        print(f"Found {len(all_tracks)} tracks by AC/DC")
        print("Sample tracks:")
        for track in all_tracks[:5]:  # Show first 5 tracks
            print(f"- {track['Name']} (Album ID: {track['AlbumId']})")
        
        # Example 2: Find the top 5 genres by number of tracks
        print("\nExample 2: Find the top 5 genres by number of tracks")
        print("--------------------------------------------------")
        
        # Step 1: Get all genres
        result = await client.call_tool("get_all_records", {"table_name": "Genre", "limit": 100})
        genres = json.loads(result[0].text)
        print(f"Found {len(genres)} genres")
        
        # Step 2: Get all tracks
        result = await client.call_tool("get_all_records", {"table_name": "Track", "limit": 1000})
        tracks = json.loads(result[0].text)
        print(f"Analyzing {len(tracks)} tracks")
        
        # Step 3: Count tracks per genre
        genre_counts = {}
        for genre in genres:
            genre_id = genre['GenreId']
            genre_name = genre['Name']
            count = len([track for track in tracks if track['GenreId'] == genre_id])
            genre_counts[genre_name] = count
        
        # Step 4: Sort and display top 5
        top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        print("\nTop 5 genres by number of tracks:")
        for i, (genre_name, count) in enumerate(top_genres, 1):
            print(f"{i}. {genre_name}: {count} tracks")
        
        # Example 3: Find the total duration of all tracks by AC/DC
        print("\nExample 3: Find the total duration of all tracks by AC/DC")
        print("-----------------------------------------------------")
        
        total_milliseconds = sum(track['Milliseconds'] for track in all_tracks)
        total_seconds = total_milliseconds / 1000
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        
        print(f"Total duration of all AC/DC tracks: {hours} hours, {minutes} minutes, {seconds} seconds")
        print(f"Total tracks: {len(all_tracks)}")
        print(f"Average track length: {total_milliseconds / len(all_tracks) / 1000:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(mcp_complex_queries())
