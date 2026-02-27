import difflib          # Ger sequenceMatcher för likhetsmått (0..1), för att få bästa matchningen på strängar
import unicodedata      # För att normalisera Unicode 

def norm(input_string: str) -> str:
    """
    Normaliserar en sträng för jämförelse:
    - Unicode-normalisering (NFKC) så likartade tecken blir jämförbara
    - casefold() för robust gemen (bättre än lower() för internationella tecken)
    - klipper bort extra mellanrum (gör multipla mellanslag till ett)
    """
    input_string = unicodedata.normalize("NFKC", input_string).casefold()  # Normalisera unicode + gör allt gemener (casefold)
    return " ".join(input_string.split())                       # Dela på whitespace och sätt ihop 

def token_set_ratio(text_a: str, text_b: str) -> int:
    """
    Ordningsoberoende jämförelse som liknar fuzz.token_set_ratio:
    - Delar upp i ord (tokens) efter normalisering
    - Tittar på vilka ord som är gemensamma
    - Jämför 'common' mot helheten för att få ett robust mått (0..100)
    Obs: Detta är enkelt men effektivt för namn och korta fraser.
    """
    # Normalisera och dela upp i ord
    tokens_in_a = set(norm(text_a).split())                  # Mängd ord i a (ordningsoberoende)
    tokens_in_b = set(norm(text_b).split())                  # Mängd ord i b

    # Gemensamma ord
    common = " ".join(sorted(tokens_in_a & tokens_in_b))   # Sträng av gemensamma ord (sorterad för stabilitet)

    # Hela token-mängderna som strängar (för jämförelse)
    all_tokens_in_a = " ".join(sorted(tokens_in_a))               # alla ord i a som en sträng
    all_tokens_in_b = " ".join(sorted(tokens_in_b))               # alla ord i b som en sträng

    # Jämför 'common' mot vardera helhet med SequenceMatcher (ger värde 0..1)
    similarity_ratio_vs_a_all = difflib.SequenceMatcher(None, common, all_tokens_in_a).ratio()
    similarity_ratio_vs_b_all = difflib.SequenceMatcher(None, common, all_tokens_in_b).ratio()

    # Ta det bästa av de två och skala till 0..100 som int
    return int(100 * max(similarity_ratio_vs_a_all, similarity_ratio_vs_b_all))

#Metoden i main 
def best_match(query: str, candidates: list[str], cutoff: int = 82):
    """Exakt → prefix per ord → substring per ord → fuzzy (token_set_ratio)."""
    query_norm = norm(query)
    normalized_candidates = [norm(candidate_string) for candidate_string in candidates]

    # Exakt
    if query_norm in normalized_candidates:
        exact_index = normalized_candidates.index(query_norm)
        return candidates[exact_index], 100, exact_index

    query_tokens = query_norm.split()

    # Prefix per ord
    for index, candidate_norm in enumerate(normalized_candidates):
        candidate_tokens = candidate_norm.split()
        if all(any(candidate_token.startswith(query_token) for candidate_token in candidate_tokens)
               for query_token in query_tokens):
            return candidates[index], 95, index

    # Substring per ord
    for index, candidate_norm in enumerate(normalized_candidates):
        candidate_tokens = candidate_norm.split()
        if all(any(query_token in candidate_token for candidate_token in candidate_tokens)
               for query_token in query_tokens):
            return candidates[index], 93, index

    # Fuzzy
    scored_candidates = [(token_set_ratio(query, candidate_string), index)
                         for index, candidate_string in enumerate(candidates)]
    highest_score, best_index = max(scored_candidates, default=(0, -1))
    if highest_score >= cutoff:
        return candidates[best_index], highest_score, best_index
    return None






