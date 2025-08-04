from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

Splitter = RecursiveCharacterTextSplitter


def get_splitter(chunk_size: int) -> Splitter:
    """Returns a token-based text splitter with overlap.

    Args:
        chunk_size (int): Number of tokens per chunk.

    Returns:
        Splitter: A text splitter instance that splits input text into overlapping chunks based on token count.
    """

    chunk_overlap = int(0.15 * chunk_size)

    logger.info(
        f"Getting splitter with chunk size: {chunk_size} and overlap: {chunk_overlap}"
    )

    return RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
