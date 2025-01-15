from flask import Flask, request, send_file
import ezdxf
from io import BytesIO

app = Flask(__name__)

@app.route('/generate-dxf', methods=['POST'])
def generate_dxf():
    data = request.get_json()
    length = float(data['length'])
    width = float(data['width'])

    # Create a new DXF document
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()

    # Check if length and width are positive, otherwise return an error
    if length <= 0 or width <= 0:
        return "Length and width must be positive values", 400

    # Add a rectangle using four points
    msp.add_lwpolyline([(0, 0), (length, 0), (length, width), (0, width)], close=True)

    # Save DXF to a BytesIO object
    output = BytesIO()
    doc.write(output)  # Ensure we write the document to the BytesIO object
    output.seek(0)

    # Send the file to the client
    return send_file(output, as_attachment=True, download_name="rectangle.dxf", mimetype="application/dxf")

if __name__ == '__main__':
    app.run(debug=True)
