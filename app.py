import streamlit as st
import pandas as pd
import grpc
import trustlevel_pb2
import trustlevel_pb2_grpc
import service  # Import service file to connect with the bias service
import config   # Import config file for necessary configurations

# Function to call the TrustLevel Bias service for each article
def get_bias_score(article_text):
    try:
        # Connect to the TrustLevel Bias service using the provided gRPC code
        channel = grpc.insecure_channel(config.SNET_ENDPOINT)
        stub = trustlevel_pb2_grpc.TrustLevelStub(channel)
        request = trustlevel_pb2.ArticleRequest(article=article_text)
        response = stub.GetBiasScore(request)
        return response.score
    except Exception as e:
        st.error(f"Error processing article: {e}")
        return None

# Streamlit UI
st.title("TrustLevel Bias Detector")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file with news articles", type=["csv"])

# Process the uploaded file
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    if 'title' in df.columns and 'text' in df.columns:
        st.write("Uploaded CSV Preview:")
        st.dataframe(df.head())

        # Prepare a new column for bias scores
        df['bias_score'] = None

        # Loop over each article and get the bias score
        for index, row in df.iterrows():
            article_text = f"{row['title']} {row['text']}"  # Combine title and text for analysis
            bias_score = get_bias_score(article_text)  # Call the service
            df.at[index, 'bias_score'] = bias_score

        # Display results in a table
        st.subheader("Bias Scores for Articles")
        st.dataframe(df[['title', 'bias_score']])

        # Option to download results as a CSV file
        csv = df.to_csv(index=False)
        st.download_button(label="Download results as CSV", data=csv, mime="text/csv")
    else:
        st.error("The uploaded CSV must contain 'title' and 'text' columns.")