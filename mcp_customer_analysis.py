

import asyncio
import json
from fastmcp import Client
from collections import Counter

async def mcp_customer_analysis():
    print("Chinook MCP Customer Analysis Demo")
    print("=================================\n")
    
    # Connect to the MCP server
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        # Example: Find customers who purchased AC/DC tracks
        print("Finding customers who purchased AC/DC tracks")
        print("-------------------------------------------")
        
        # Step 1: Get AC/DC's artist info
        result = await client.call_tool("get_record", {"table_name": "Artist", "record_id": 1})
        artist = json.loads(result[0].text)
        artist_name = artist["Name"]
        print(f"Artist: {artist_name} (ID: {artist['ArtistId']})")
        
        # Step 2: Get all albums by AC/DC
        result = await client.call_tool("get_all_records", {"table_name": "Album", "limit": 100})
        all_albums = json.loads(result[0].text)
        artist_albums = [album for album in all_albums if album['ArtistId'] == artist['ArtistId']]
        album_ids = [album['AlbumId'] for album in artist_albums]
        print(f"Found {len(artist_albums)} albums by {artist_name}")
        
        # Step 3: Get all tracks from those albums
        result = await client.call_tool("get_all_records", {"table_name": "Track", "limit": 1000})
        all_tracks = json.loads(result[0].text)
        artist_tracks = [track for track in all_tracks if track['AlbumId'] in album_ids]
        track_ids = [track['TrackId'] for track in artist_tracks]
        print(f"Found {len(artist_tracks)} tracks by {artist_name}")
        
        # Step 4: Get all invoice lines containing those tracks
        result = await client.call_tool("get_all_records", {"table_name": "InvoiceLine", "limit": 2000})
        all_invoice_lines = json.loads(result[0].text)
        artist_invoice_lines = [line for line in all_invoice_lines if line['TrackId'] in track_ids]
        invoice_ids = [line['InvoiceId'] for line in artist_invoice_lines]
        print(f"Found {len(artist_invoice_lines)} invoice lines for {artist_name} tracks")
        
        # Step 5: Get all invoices for those invoice lines
        result = await client.call_tool("get_all_records", {"table_name": "Invoice", "limit": 1000})
        all_invoices = json.loads(result[0].text)
        artist_invoices = [invoice for invoice in all_invoices if invoice['InvoiceId'] in invoice_ids]
        customer_ids = [invoice['CustomerId'] for invoice in artist_invoices]
        print(f"Found {len(artist_invoices)} invoices containing {artist_name} tracks")
        
        # Step 6: Get customer information
        result = await client.call_tool("get_all_records", {"table_name": "Customer", "limit": 100})
        all_customers = json.loads(result[0].text)
        artist_customers = [customer for customer in all_customers if customer['CustomerId'] in customer_ids]
        
        # Count purchases per customer
        customer_purchase_counts = Counter(customer_ids)
        
        # Create a list of customers with their purchase counts
        customers_with_counts = []
        for customer in artist_customers:
            customer_id = customer['CustomerId']
            purchase_count = customer_purchase_counts[customer_id]
            customers_with_counts.append({
                'CustomerId': customer_id,
                'FirstName': customer['FirstName'],
                'LastName': customer['LastName'],
                'Country': customer['Country'],
                'PurchaseCount': purchase_count
            })
        
        # Sort by purchase count (descending)
        customers_with_counts.sort(key=lambda x: x['PurchaseCount'], reverse=True)
        
        # Display results
        print(f"\nFound {len(artist_customers)} customers who purchased {artist_name} tracks")
        print("\nTop 10 customers by purchase count:")
        for i, customer in enumerate(customers_with_counts[:10], 1):
            print(f"{i}. {customer['FirstName']} {customer['LastName']} ({customer['Country']}): {customer['PurchaseCount']} purchases")
        
        # Analyze customer countries
        country_counts = Counter([customer['Country'] for customer in artist_customers])
        print("\nCustomer distribution by country:")
        for country, count in country_counts.most_common(5):
            print(f"- {country}: {count} customers")

if __name__ == "__main__":
    asyncio.run(mcp_customer_analysis())

