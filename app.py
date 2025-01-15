from flask import Flask, request, send_file
import ezdxf
from io import BytesIO

app = Flask(__name__)

@app.route('/generate-dxf', methods=['POST'])
def generate_dxf():
    data = request.get_json()
    length = float(data['length'])
    width = float(data['width'])

    # Validate length and width to ensure they are positive numbers
    if length <= 0 or width <= 0:
        return "Length and width must be positive values", 400

    # Create a new DXF document
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()

    # Add a rectangle using 4 points, making sure we close the polyline
    msp.add_lwpolyline([(0, 0), (length, 0), (length, width), (0, width)], close=True)

    # Debug: Print the entities added to the DXF file
    print("Entities in the DXF file:", doc.entities)

    # Create a BytesIO object to save the file content into memory
    output = BytesIO()
    
    # Save the DXF file to the in-memory buffer
    doc.write(output)
    output.seek(0)

    # Return the generated DXF file as an attachment
    return send_file(output, as_attachment=True, download_name="rectangle.dxf", mimetype="application/dxf")

if __name__ == '__main__':
    app.run(debug=True)
