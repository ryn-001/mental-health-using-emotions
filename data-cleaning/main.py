from cleaning_phases.language_detection_and_filtering import filter_english_text;
from cleaning_phases.noise_removal import noise_removal;
from cleaning_phases.social_media_text_normalization import social_media_text_normalization;
from cleaning_phases.spam_bot_filtering import spam_bot_filtering;
from cleaning_phases.structural_cleaning import structural_cleaning;
from cleaning_phases.unicode_and_encoding_normalization import unicode_and_encoding_normalization;
from cleaning_phases.whitespace_normalization import whitespace_normalization;
from utils.load_df_from_path import load_df_from_path
from utils.save_df_to_path import append_df_to_path

df = load_df_from_path()

# Cleaning Phases
df = structural_cleaning(df)
df = unicode_and_encoding_normalization(df)
df = whitespace_normalization(df)
df = filter_english_text(df)
df = noise_removal(df)
df = social_media_text_normalization(df)
df = spam_bot_filtering(df)

append_df_to_path(df)



