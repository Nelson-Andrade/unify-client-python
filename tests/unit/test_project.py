from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.project.resource import Project


class TestProject(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_project_add_input_dataset(self):
        responses.add(responses.GET, self.datasets_url, json=self.dataset_json)
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        responses.add(
            responses.POST,
            self.input_datasets_url,
            json=self.post_input_datasets_json,
            status=204,
        )
        responses.add(
            responses.GET, self.input_datasets_url, json=self.get_input_datasets_json
        )

        dataset = self.unify.datasets.by_external_id(self.dataset_external_id)
        project = self.unify.projects.by_external_id(self.project_external_id)
        project.add_input_dataset(dataset)
        alias = project.api_path + "/inputDatasets"
        input_datasets = project.client.get(alias).successful().json()
        self.assertEqual(self.dataset_json, input_datasets)

    @responses.activate
    def test_project_by_external_id__raises_when_not_found(self):
        responses.add(responses.GET, self.projects_url, json=[])
        with self.assertRaises(KeyError):
            self.unify.projects.by_external_id(self.project_external_id)

    @responses.activate
    def test_project_by_external_id_succeeds(self):
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        actual_project = self.unify.projects.by_external_id(self.project_external_id)
        self.assertEqual(self.project_json[0], actual_project._data)

    @responses.activate
    def test_project_attributes_get(self):
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        responses.add(
            responses.GET,
            self.project_attributes_url,
            json=self.project_attributes_json,
        )
        project = self.unify.projects.by_external_id(self.project_external_id)
        attributes = list(project.attributes)
        self.assertEqual(len(self.project_attributes_json), len(attributes))
        id_attribute = project.attributes.by_name("id")
        self.assertEqual(self.project_attributes_json[0]["name"], id_attribute.name)

    @responses.activate
    def test_project_attributes_post(self):
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        responses.add(
            responses.GET,
            self.project_attributes_url,
            json=self.project_attributes_json,
        )
        responses.add(
            responses.POST,
            self.project_attributes_url,
            json=self.project_attributes_json[0],
            status=204,
        )
        project = self.unify.projects.by_external_id(self.project_external_id)
        # project.attributes.create MUST make a POST request to self.project_attributes_url
        # If it posts to some other URL, responses will raise an exception;
        # If it does not post to any URL, responses will also raise an exception.
        project.attributes.create(self.project_attributes_json[0])

    def test_project_get_input_datasets(self):
        p = Project(self.unify, self.project_json[0])
        datasets = p.input_datasets()
        self.assertEqual(datasets.api_path, "projects/1/inputDatasets")

    dataset_external_id = "1"
    datasets_url = f"http://localhost:9100/api/versioned/v1/datasets?filter=externalId=={dataset_external_id}"
    dataset_json = [
        {
            "id": "unify://unified-data/v1/datasets/1",
            "externalId": "1",
            "name": "dataset 1 name",
            "description": "dataset 1 description",
            "version": "dataset 1 version",
            "keyAttributeNames": ["tamr_id"],
            "tags": [],
            "created": {
                "username": "admin",
                "time": "2018-09-10T16:06:20.636Z",
                "version": "dataset 1 created version",
            },
            "lastModified": {
                "username": "admin",
                "time": "2018-09-10T16:06:20.851Z",
                "version": "dataset 1 modified version",
            },
            "relativeId": "datasets/1",
            "upstreamDatasetIds": [],
        }
    ]
    project_json = [
        {
            "id": "unify://unified-data/v1/projects/1",
            "externalId": "project 1 external ID",
            "name": "project 1 name",
            "description": "project 1 description",
            "type": "DEDUP",
            "unifiedDatasetName": "project 1 unified dataset",
            "created": {
                "username": "admin",
                "time": "2018-09-10T16:06:20.636Z",
                "version": "project 1 created version",
            },
            "lastModified": {
                "username": "admin",
                "time": "2018-09-10T16:06:20.851Z",
                "version": "project 1 modified version",
            },
            "relativeId": "projects/1",
        }
    ]
    project_external_id = "project 1 external ID"
    projects_url = f"http://localhost:9100/api/versioned/v1/projects?filter=externalId=={project_external_id}"
    post_input_datasets_json = []
    input_datasets_url = (
        f"http://localhost:9100/api/versioned/v1/projects/1/inputDatasets"
    )
    get_input_datasets_json = dataset_json

    project_attributes_url = (
        "http://localhost:9100/api/versioned/v1/projects/1/attributes"
    )
    project_attributes_json = [
        {
            "name": "id",
            "description": "identifier",
            "type": {"baseType": "STRING"},
            "isNullable": False,
        },
        {
            "name": "name",
            "description": "full name",
            "type": {"baseType": "ARRAY", "innerType": {"baseType": "STRING"}},
            "isNullable": True,
        },
        {
            "name": "description",
            "description": "human readable description",
            "type": {"baseType": "ARRAY", "innerType": {"baseType": "STRING"}},
            "isNullable": True,
        },
    ]
