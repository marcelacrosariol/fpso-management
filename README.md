# fpso-management
My solution for MODEC's back-end developer assignment. The API manages different equipment of an FPSO (Floating Production, Storage and Offloading).

# Table of contents
1. [Technologies](#technologies)
2. [Project Structure](#project_structure)
3. [Local Setup](#localsetup)
4. [Initialize](#project_run)
5. [Endpoints](#endpoints)
    - [List vessels](#vessel_list)
    - [Create vessel](#vessel_create)
    - [List vessel's equipment](#vessel_equipment_list)
    - [Register an equipment on a vessel](#vessel_equipment_register)
    - [Activate equipament(s)](#equipment_activate)
    - [Deactivate equipament(s)](#equipment_deactivate)
6. [Run tests](#tests)

## Technologies <a name="technologies"></a>
    - Docker
    - Django
    - Django REST Framework
    - SQLite3

## Project Structure <a name="project_structure"></a>

![Project Structure](https://github.com/marcelacrosariol/fpso-management/blob/main/docs/img/01_project_structure.PNG?raw=true)

1. Django Project
2. appmanagement module
3. fpso module
4. Docker configuration files

## Setup <a name="localsetup"></a>

If you do not have Docker yet, [ install the Engine and Compose ](https://docs.docker.com/get-docker/).

Once you have done it, fork and clone/download the project on your machine.

Before building a Docker image, you must create a `.env` file on the fpso-management root directory. It will be used in order to define the environment variables inside the container and it is called on `docker-compose.yml`. The file must contain the following parameters.

```
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
DEBUG=1
```

If your operating system is Windows 10 Home or any other that requires the Docker Toolbox, you will also need to add the 'DOCKER_IP_HOST' variable with the IP used by the `default` virtual machine instance. _(You can find the correct IP with the command ```docker-machine default ip```)._

```
DOCKER_IP_HOST=<DOCKER_MACHINE_IP>
```

Next, run the following command to build the image that will be the template for the container.

```shell
$ docker-compose build
```

After the process finish all the instructions from the Dockerfile, run the migrations to create and set up the database.


```shell
$ docker exec -it fpso-management-main_app_1 ./manage.py migrate
```

## Initialize <a name="project_run"></a>

Run the container and launch the local server using the following command.

```shell
docker-compose up
```

## Endpoints <a name="endpoints"></a>

### `/fpso/vessel/` <a name="vessel_list"></a>
<_List vessels_>

**Method** : `GET`

**Auth required** : `NO`

**URL Params (optional)**: `search=[code]`

### Success Response

**Code** : `200 OK`

**Content example**
```json
[
    {
        "code": "CV001"
    },
    {
        "code": "CV002"
    },
    {
        "code": "CV003"
    }
]
```
-------------------------------------------------------------------------------

### `/fpso/vessel/create/` <a name="vessel_create"></a>
<_Create vessel_>

**Method** : `POST`

**Auth required** : `NO`

**Data constraints**

```json
{
    "code": "[ Alphanumeric up to 10 characters ]"
}
```

**Data example**

```json
{
    "code": "CV200"
}
```

### Success Response

**Code** : `201 CREATED`

**Content example**

```json
{
    "code": "CV200"
}
```

### Error Response

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "code": [
        "Ensure this field has no more than 10 characters."
    ]
}
```
-------------------------------------------------------------------------------

### `/fpso/vessel/<code>/equipments/` <a name="vessel_equipment_list"></a>
<_List vessel's equipment_>

**Method** : `GET`

**Auth required** : `NO`

**URL Params (optional)**: `search=[status(active|inactive)]` 

### Success Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "name": "Compressor",
        "code": "CC001",
        "location": "Brazil",
        "status": "Active"
    },
    {
        "name": "Compressor",
        "code": "CC002",
        "location": "Brazil",
        "status": "Active"
    },
    {
        "name": "Compressor",
        "code": "CC003",
        "location": "Brazil",
        "status": "Active"
    }
]
```

### Error Response

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "code": [
        "Vessel matching query does not exist."
    ]
}
```

-------------------------------------------------------------------------------
### `/fpso/vessel/<code>/register/` <a name="vessel_equipment_register"></a>
<_Register an equipment on a vessel_>

**Method** : `POST`

**Auth required** : `NO`

**Data constraints**

```json
{
    "name": "[ String up to 40 characters ]",
    "code": "[ Alphanumeric up to 10 characters ]",
    "location": "[ String up to 10 characters ]"
}
```

**Data example**

```json
{
    "name": "Compressor",
    "code": "5310B9D7",
    "location": "Brazil"
}
```

### Success Response

**Code** : `201 CREATED`

**Content example**
```json
{
    "name": "Compressor",
    "code": "5310B9D7",
    "location": "Brazil"
}
```

### Error Response

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "code": [
        "Code must be alphanumeric."
    ]
}
```
-------------------------------------------------------------------------------
### `/fpso/equipments/activate/` <a name="equipment_activate"></a>
<_Activate equipament_>

**Method** : `PUT`

**Auth required** : `NO`

**Data constraints**

```json
{
    "codes": [ "A list of one or more codes."]
}
```

**Data example**

```json
{
    "codes": ["5310B9D7"]
}
```

### Success Response

**Code** : `200 OK`

**Content example**
```json
[
    {
        "name": "Compressor",
        "code": "5310B9D7",
        "location": "Brazil",
        "status": "Active"
    }
]
```

### Error Response

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "code": [
        "Equipment matching query does not exist."
    ]
}
```
-------------------------------------------------------------------------------
### `/fpso/equipments/deactivate/` <a name="equipment_deactivate"></a>
<_Deactivate equipament_>

**Method** : `PUT`

**Auth required** : `NO`

**Data constraints**

```json
{
    "codes": [ "A list of one or more codes."]
}
```

**Data example**

```json
{
    "codes": ["5310B9D7"]
}
```

### Success Response

**Code** : `200 OK`

**Content example**
```json
[
    {
        "name": "Compressor",
        "code": "5310B9D7",
        "location": "Brazil",
        "status": "Inactive"
    }
]
```

### Error Response

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
    "code": [
        "Equipment matching query does not exist."
    ]
}
```

## Run tests <a name="tests"></a>
```
docker exec -it <container_name> ./manage.py test --verbosity=2]
```
