import pandas as pd

ALLOWED_EXTENSIONS = {'csv', 'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_eob_file(file_path, file_extension):
    """ Process file and return summary + first 5 rows for preview. """
    try:
        if file_extension == 'csv':
            df = pd.read_csv(file_path)
        elif file_extension == 'json':
            df = pd.read_json(file_path)
        else:
            return {"error": "Unsupported file format"}

        # Extract first 5 rows for preview
        preview = {
            "headers": df.columns.tolist(),
            "rows": df.head(5).values.tolist()
        }
        return preview

    except Exception as e:
        return {"error": str(e)}