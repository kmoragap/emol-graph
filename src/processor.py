from collections import Counter
from itertools import combinations

import pandas as pd
import spacy
from tqdm import tqdm

from config import BLACKLIST, ENTITY_MAPPING, PROCESSED_DATA_PATH, RAW_DATA_PATH


class GraphProcessor:
    def __init__(self, model_name="es_core_news_lg"):
        print("Loading NLP model...")
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Model {model_name} not found. Please download it first.")
            raise

    def normalize_entity(self, name):
        """Cleans and standardizes entity names."""
        clean_name = name.strip().replace("\n", " ")

        # Check mapping (e.g., 'Presidente Boric' -> 'Gabriel Boric')
        if clean_name in ENTITY_MAPPING:
            return ENTITY_MAPPING[clean_name]

        return clean_name

    def extract_entities(self, text):
        """Finds People and Organizations in text."""
        doc = self.nlp(text)
        entities = set()

        for ent in doc.ents:
            if ent.label_ in ["PER", "ORG"] and ent.text not in BLACKLIST:
                name = self.normalize_entity(ent.text)

                # Filter out short noise or lowercase errors
                if len(name) > 3 and name[0].isupper():
                    entities.add(name)

        return list(entities)

    def build_graph(self):
        """Reads raw news, extracts entities, and builds the edge list."""
        print("Reading raw data...")
        try:
            df = pd.read_csv(RAW_DATA_PATH)
        except FileNotFoundError:
            print("Raw data not found. Run scraper.py first.")
            return

        relationships = []

        print("Processing articles (NLP)...")
        for _, row in tqdm(df.iterrows(), total=len(df)):
            # Combine title and body for full context
            full_text = f"{row['title']}. {row['body']}"

            if len(full_text) < 50:
                continue

            ents = self.extract_entities(full_text)

            # If two entities appear in the same article, create a link
            if len(ents) > 1:
                pairs = list(combinations(sorted(ents), 2))
                relationships.extend(pairs)

        # Count occurrences (Weight of the relationship)
        counts = Counter(relationships)

        # Prepare DataFrame
        graph_data = [
            {"source": k[0], "target": k[1], "weight": v} for k, v in counts.items()
        ]

        df_graph = pd.DataFrame(graph_data)
        df_graph.to_csv(PROCESSED_DATA_PATH, index=False)
        print(f"Graph processing complete. Edges saved to {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    processor = GraphProcessor()
    processor.build_graph()
