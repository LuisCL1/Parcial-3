from flask import Blueprint, Response



appcsv=Blueprint("appcsv",__name__,template_folder="templates")
def generate_csv():
    # Create a CSV string or generate data dynamically
    csv_data = [
        ['Name', 'Age', 'Country'],
        ['John', '25', 'USA'],
        ['Alice', '30', 'Canada'],
        ['Bob', '28', 'UK']
    ]
    
    # Create a generator to yield CSV rows
    def generate():
        for row in csv_data:
            yield ','.join(row) + '\n'
    
    # Set response headers to indicate CSV content
    headers = {
        'Content-Disposition': 'attachment; filename=data.csv',
        'Content-Type': 'text/csv'
    }
    
    # Return a Flask response object with the CSV generator
    return Response(generate(), headers=headers)

@app.route('/download-csv')
def download_csv():
    return generate_csv()
