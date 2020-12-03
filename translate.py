from google.cloud import translate


def batch_translate_text(
    input_uri, output_uri_prefix, project_id, location, source_lang, target_lang
):
    """
    Example:
    input_uri: "gs://tempbucket/pfe/pfe.en-US.txt"
    output_uri_prefix: "gs://tempbucket/pfe-translated/"
    project_id: myproject_id
    location: us-central1  # global location is not supported by batch translate api
    source_lang: en
    target_lang: zn
        # Translate language code: https://cloud.google.com/translate/docs/languages
    """
    # call batch translate against orig.txt
    client = translate.TranslationServiceClient()
    gcs_source = {"input_uri": input_uri}
    input_configs_element = {"gcs_source": gcs_source, "mime_type": "text/plain"}
    gcs_destination = {"output_uri_prefix": output_uri_prefix}
    output_config = {"gcs_destination": gcs_destination}
    parent = f"projects/{project_id}/locations/{location}"

    operation = client.batch_translate_text(
        request={
            "parent": parent,  # Required para
            "source_language_code": source_lang,
            "target_language_codes": [target_lang],  # Up to 10 language codes here.
            "input_configs": [input_configs_element],
            "output_config": output_config,
        }
    )

    print("Translating...", input_uri)
    response = operation.result(timeout=3600)

    print(input_uri, "Total Characters: {}".format(response.total_characters), u"Translated: {}".format(response.translated_characters))


