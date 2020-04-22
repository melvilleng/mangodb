@@ -88,12 +88,12 @@ def add_checkups(animal_id):
    vet = client[DB_NAME].vets.find_one({
        "_id": ObjectId(request.form.get('vet'))
    })
    print(vet)
    animal = client[DB_NAME].animals.update({
        "_id": ObjectId(animal_id)
    }, {
        "$push": {
            'checkups': {
                "checkup_id": ObjectId(),
                "vet_id": vet['_id'],
                "vet": vet['name'],
                "diagnosis": request.form.get("diagnosis"),
@@ -103,26 +103,70 @@ def add_checkups(animal_id):
    })
    return redirect(url_for('show_checkups_for_animal', animal_id=animal_id))

@app.route("/delete_checkups/<animal_id>/<date>")
@app.route("/delete_checkups/<animal_id>/<checkup_id>")
def delete_checkup(animal_id, checkup_id):
    client[DB_NAME].animals.update({
        "_id":ObjectId(animal_id)
        "_id": ObjectId(animal_id)
    }, {
        '$pull':{
        '$pull': {
            'checkups': {

                "checkup_id": ObjectId(checkup_id)
            }
        }
    })
    return redirect(url_for('show_checkups_for_animal', animal_id=animal_id))

@app.route("/delete_animal/<animal_id>")
def delete_animal(animal_id):
    client[DB_NAME].animals.remove({
        "_id":ObjectId(animal_id)
        "_id": ObjectId(animal_id)
    })
    return redirect(url_for('show_animals'))


@app.route("/edit_checkup/<checkup_id>")
def edit_checkup(checkup_id):

    # grab the vets
    vets = client[DB_NAME].vets.find()

    # retrieve the checkup
    checkup = client[DB_NAME].animals.find_one({
        'checkups.checkup_id': ObjectId(checkup_id)
    }, {
        'checkups': {'$elemMatch': {
            'checkup_id': ObjectId(checkup_id)
        }}
    })['checkups'][0]

    return render_template('edit_checkup.template.html',
                           checkup=checkup,
                           vets=vets)


@app.route('/edit_checkup/<checkup_id>', methods=["POST"])
def process_edit_checkup(checkup_id):

    vet = client[DB_NAME].vets.find_one({
        '_id': ObjectId(request.form.get('vet'))
    })

    animal = client[DB_NAME].animals.find_one({
          "checkups.checkup_id": ObjectId(checkup_id)
    })

    client[DB_NAME].animals.update({
        "checkups.checkup_id": ObjectId(checkup_id)
    }, {
        '$set': {
            'checkups.$.vet_id': request.form.get('vet_id'),
            'checkups.$.vet': vet['name'],
            'checkups.$.diagnosis': request.form.get('diagnosis'),
            'checkups.$.date': datetime.datetime.strptime(request.form.get('date'), "%Y-%m-%d")
        }
    })
    return redirect(url_for('show_checkups_for_animal', animal_id=animal['_id']))

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
 29  animal_shelter_app/templates/edit_checkup.template.html 
@@ -0,0 +1,29 @@
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    {{checkup}}
      <form method="POST">
        <label>Vet</label>
        <select name="vet" value='{{checkup.vet}}'>
            {% for v in vets %}
            <option value="{{v._id}}" {%if checkup.vet_id == v._id %}selected{%endif%}>
                {{v.name}} from {{v.clinic}}
            </option>
            {%endfor%}
        </select>
        <br/>
        <label>Diagnosis</label>
        <input type="text" name="diagnosis" value='{{checkup.diagnosis}}'/>
        <br/>
        <label>Date:</label>
        <input type="date" name="date" value='{{checkup.date.strftime("%Y-%m-%d")}}'/>
        <input type="submit"/>
    </form> 
</body>
</html> 
 2  animal_shelter_app/templates/show_checkups.template.html 
@@ -14,6 +14,8 @@ <h1>Showing checkups for {{animal.name}}</h1>
        <li>{{ c.date}}</li>
        <li>{{ c.vet}}</li>
        <li>{{ c.diagnosis}}</li>
        <li><a href="{{ url_for('edit_checkup', checkup_id = c.checkup_id) }}">Edit</a>
        <li><a href="{{ url_for('delete_checkup', animal_id=animal._id, checkup_id=c.checkup_id) }}">Delete</a>
    </ul>
    {%else%}
        No checkups have been made
 0  walkthrough/animal-shelter.json → data/walkthrough/animal-shelter.json 
File renamed without changes.
 0  walkthrough/animals.json → data/walkthrough/animals.json 
File renamed without changes.
 0  walkthrough/checkups.json → data/walkthrough/checkups.json 
File renamed without changes.
 0  walkthrough/conditions.json → data/walkthrough/conditions.json 
File renamed without changes.
 16  walkthrough/queries.md → data/walkthrough/queries.md 
@@ -243,4 +243,18 @@ Update an animal piecemeal (only replacing what is specified). Example: to chang
Delete
    db.animals.remove({
        _id:ObjectId("5e9e5cc77fb3bf5da545666a")
    })
    })
## Create vets
    db.vets.insertMany([
        {
            "name":"Dr Chua",
            "license":"X123456",
            "clinic":"Sunshine Way Pet Clinic"
        },
        {
            "name":"Dr. Leon",
            "license":"ABC12345",
            "clinic":"Animal Hospital"
        }
    ])