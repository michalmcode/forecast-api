import io

import boto3


def upload_file(bytes: io.BytesIO, filename: str) -> None:
    """Upload a file to an S3 bucket

    Args:
        bytes (io.BytesIO): Raw data
        filename (str): The name of the file
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("forecast-api-flask")

    bucket.upload_fileobj(bytes, filename)


def download_file(filename: str) -> io.BytesIO:
    """Download a file from an S3 bucket

    Args:
        filename (str): The name of the file

    Returns:
        io.BytesIO: The raw data
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("forecast-api-flask")

    data = io.BytesIO()
    bucket.download_fileobj(filename, data)
    data.seek(0)
    return data
