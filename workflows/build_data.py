import asyncio
import os
import sys

from googletrans import Translator
from utils import File, JSONFile, Log

log = Log("i18n")


async def translate_phrases(phrases, lang, current_idx):
    translator = Translator()
    idx = {}
    n = len(phrases)
    for i, phrase in enumerate(phrases):
        if lang == "en":
            idx[phrase] = phrase
            continue

        if phrase in current_idx:
            idx[phrase] = current_idx[phrase]
            continue

        try:

            translation = await translator.translate(
                phrase, src="en", dest=lang
            )
            idx[phrase] = translation.text
            log.debug(
                f"☑️ {lang}/{i}/{n})" + f" '{phrase}' -> '{translation.text}'"
            )
        except Exception as e:
            log.error(f"❌ {lang}/{i}/{n})" + f" '{phrase}' FAILED")
            idx[phrase] = phrase

    return idx


def main(dir_path):
    phrases_file = File(os.path.join(dir_path, "en.txt"))
    original_phrases = File(os.path.join(dir_path, "en.txt")).read_lines()
    phrases = [p.strip() for p in original_phrases if p.strip()]
    phrases = list(set(phrases))
    phrases.sort()
    if phrases != original_phrases:
        phrases_file.write_lines(phrases)
        log.info(f"Updated {phrases_file}")

    log.debug(f"Read {len(phrases)} phrases from en.txt")

    for lang in ["en", "si", "ta"]:
        lang_idx_path = os.path.join(dir_path, f"{lang}.json")
        lang_idx_json_file = JSONFile(lang_idx_path)
        current_idx = lang_idx_json_file.read()
        idx = asyncio.run(translate_phrases(phrases, lang, current_idx))

        lang_idx_json_file.write(idx)
        log.info(f"Wrote {lang_idx_json_file}")


if __name__ == "__main__":
    main(dir_path=sys.argv[1])
