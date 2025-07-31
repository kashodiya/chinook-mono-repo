

import asyncio
from fastmcp import Client
import json

async def main():
    # Connect to the MCP server
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        print("=== Chinook Database MCP Client Test ===\n")
        
        # 1. List all tables
        print("1. Listing all tables:")
        result = await client.call_tool("list_tables")
        tables = json.loads(result[0].text)["tables"]
        print(f"Available tables: {', '.join(tables)}")
        
        # 2. Get records from Artist table
        print("\n2. Getting records from Artist table:")
        result = await client.call_tool("get_all_records", {"table_name": "Artist", "limit": 3})
        artists = json.loads(result[0].text)
        for artist in artists:
            print(f"  - Artist ID: {artist['ArtistId']}, Name: {artist['Name']}")
        
        # 3. Create a new artist
        print("\n3. Creating a new artist:")
        new_artist_data = {"Name": "Test Artist"}
        result = await client.call_tool("create_record", {
            "table_name": "Artist", 
            "data": new_artist_data
        })
        create_result = json.loads(result[0].text)
        print(f"  - Create result: {create_result}")
        
        # The API returns the ID directly
        new_artist_id = create_result["id"]
        print(f"  - Created Artist ID: {new_artist_id}")
        
        # Get the newly created artist to confirm
        result = await client.call_tool("get_record", {
            "table_name": "Artist", 
            "record_id": new_artist_id
        })
        new_artist = json.loads(result[0].text)
        print(f"  - Confirmed Artist ID: {new_artist_id}, Name: {new_artist['Name']}")
        
        # 4. Get the newly created artist
        print("\n4. Getting the newly created artist:")
        result = await client.call_tool("get_record", {
            "table_name": "Artist", 
            "record_id": new_artist_id
        })
        artist = json.loads(result[0].text)
        print(f"  - Artist ID: {artist['ArtistId']}, Name: {artist['Name']}")
        
        # 5. Update the artist
        print("\n5. Updating the artist:")
        updated_data = {"Name": "Updated Test Artist"}
        result = await client.call_tool("update_record", {
            "table_name": "Artist", 
            "record_id": new_artist_id, 
            "data": updated_data
        })
        update_result = json.loads(result[0].text)
        print(f"  - Update result: {update_result}")
        
        # 6. Get the updated artist
        print("\n6. Getting the updated artist:")
        result = await client.call_tool("get_record", {
            "table_name": "Artist", 
            "record_id": new_artist_id
        })
        artist = json.loads(result[0].text)
        print(f"  - Artist ID: {artist['ArtistId']}, Name: {artist['Name']}")
        
        # 7. Delete the artist
        print("\n7. Deleting the artist:")
        result = await client.call_tool("delete_record", {
            "table_name": "Artist", 
            "record_id": new_artist_id
        })
        delete_result = json.loads(result[0].text)
        print(f"  - Delete result: {delete_result}")
        
        # 8. Try to get the deleted artist (should fail)
        print("\n8. Trying to get the deleted artist:")
        try:
            result = await client.call_tool("get_record", {
                "table_name": "Artist", 
                "record_id": new_artist_id
            })
            artist = json.loads(result[0].text)
            print(f"  - Artist still exists: {artist}")
        except Exception as e:
            print(f"  - Artist was successfully deleted: {e}")
        
        print("\n=== Test completed successfully ===")

if __name__ == "__main__":
    asyncio.run(main())

