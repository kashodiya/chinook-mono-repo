
import asyncio
import json
from fastmcp import Client

async def mcp_client_demo():
    print("Chinook MCP Client Demo")
    print("======================\n")
    
    # Connect to the MCP server
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        # List available tools
        print("Available MCP Tools:")
        print("------------------")
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
        
        # List all tables
        print("\n1. Listing all tables:")
        result = await client.call_tool("list_tables", {})
        if result and len(result) > 0:
            tables_data = json.loads(result[0].text)
            print(f"Tables: {json.dumps(tables_data['tables'], indent=2)}")
        
        # Get artists
        print("\n2. Getting first 5 artists:")
        result = await client.call_tool("get_all_records", {"table_name": "Artist", "limit": 5})
        if result and len(result) > 0:
            artists = json.loads(result[0].text)
            print(f"Artists: {json.dumps(artists, indent=2)}")
        
        # Get a specific artist
        print("\n3. Getting artist with ID 1:")
        result = await client.call_tool("get_record", {"table_name": "Artist", "record_id": 1})
        if result and len(result) > 0:
            artist = json.loads(result[0].text)
            print(f"Artist: {json.dumps(artist, indent=2)}")
        
        # Get albums for AC/DC (Artist ID 1)
        print("\n4. Getting all albums for AC/DC (Artist ID 1):")
        result = await client.call_tool("get_all_records", {"table_name": "Album", "limit": 100})
        if result and len(result) > 0:
            all_albums = json.loads(result[0].text)
            ac_dc_albums = [album for album in all_albums if album['ArtistId'] == 1]
            print(f"AC/DC Albums: {json.dumps(ac_dc_albums, indent=2)}")
            print(f"Total AC/DC Albums: {len(ac_dc_albums)}")
        
        # Create a new artist
        print("\n5. Creating a new artist:")
        result = await client.call_tool("create_record", {
            "table_name": "Artist", 
            "data": {"Name": "Test Artist"}
        })
        if result and len(result) > 0:
            create_result = json.loads(result[0].text)
            print(f"Create Result: {json.dumps(create_result, indent=2)}")
            new_artist_id = create_result.get("id")
            
            if new_artist_id:
                # Get the newly created artist
                print("\n6. Getting the newly created artist:")
                result = await client.call_tool("get_record", {"table_name": "Artist", "record_id": new_artist_id})
                if result and len(result) > 0:
                    new_artist = json.loads(result[0].text)
                    print(f"New Artist: {json.dumps(new_artist, indent=2)}")
                
                # Update the artist
                print("\n7. Updating the artist:")
                result = await client.call_tool("update_record", {
                    "table_name": "Artist", 
                    "record_id": new_artist_id,
                    "data": {"Name": "Updated Test Artist"}
                })
                if result and len(result) > 0:
                    update_result = json.loads(result[0].text)
                    print(f"Update Result: {json.dumps(update_result, indent=2)}")
                
                # Get the updated artist
                print("\n8. Getting the updated artist:")
                result = await client.call_tool("get_record", {"table_name": "Artist", "record_id": new_artist_id})
                if result and len(result) > 0:
                    updated_artist = json.loads(result[0].text)
                    print(f"Updated Artist: {json.dumps(updated_artist, indent=2)}")
                
                # Delete the artist
                print("\n9. Deleting the artist:")
                result = await client.call_tool("delete_record", {"table_name": "Artist", "record_id": new_artist_id})
                if result and len(result) > 0:
                    delete_result = json.loads(result[0].text)
                    print(f"Delete Result: {json.dumps(delete_result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(mcp_client_demo())
