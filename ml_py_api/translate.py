#!/usr/bin/env python

import argparse

from google.cloud import translate
import six


def detect_language(text):
    """Detects the text's language."""
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    print('Text: {}'.format(text))
    print('Confidence: {}'.format(result['confidence']))
    print('Language: {}'.format(result['language']))


def list_languages():
    """Lists all available languages."""
    translate_client = translate.Client()

    results = translate_client.get_languages()

    for language in results:
        print(u'{name} ({language})'.format(**language))


def list_languages_with_target(target):
    """Lists all available languages and localizes them to the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    results = translate_client.get_languages(target_language=target)

    for language in results:
        print(u'{name} ({language})'.format(**language))


def translate_text_with_model(target, text, model=translate.NMT):
    """Translates text into the target language.
    Make sure your project is whitelisted.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target, model=model)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))


def translate_text(target, text):
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    detect_langage_parser = subparsers.add_parser(
        'detect-language', help=detect_language.__doc__)
    detect_langage_parser.add_argument('text')

    list_languages_parser = subparsers.add_parser(
        'list-languages', help=list_languages.__doc__)

    list_languages_with_target_parser = subparsers.add_parser(
        'list-languages-with-target', help=list_languages_with_target.__doc__)
    list_languages_with_target_parser.add_argument('target')

    translate_text_parser = subparsers.add_parser(
        'translate-text', help=translate_text.__doc__)
    translate_text_parser.add_argument('target')
    translate_text_parser.add_argument('text')

    args = parser.parse_args()

    if args.command == 'detect-language':
        detect_language(args.text)
    elif args.command == 'list-languages':
        list_languages()
    elif args.command == 'list-languages-with-target':
        list_languages_with_target(args.target)
    elif args.command == 'translate-text':
        translate_text(args.target, args.text)
