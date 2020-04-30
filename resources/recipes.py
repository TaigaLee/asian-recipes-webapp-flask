import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required

recipes = Blueprint('recipes', 'recipes')

@recipes.route('/', methods=['GET'])
def recipes_index():
    result = models.Recipe.select().dicts()
    recipes = [recipe for recipe in result]

    recipesLength = len(recipes)

    print(recipes)

    return jsonify(
      data = recipes,
      message ="Successfully found {}".format(recipesLength),
      status = 200
    ), 200


@recipes.route('/', methods=['POST'])
@login_required
def create_recipe():
    payload = request.get_json()

    new_recipe = models.Recipe.create(
        name=payload['name'],
        poster=current_user.id,
        origin=payload['origin'],
        ingredients=payload['ingredients'],
        instructions=payload['instructions'],
    )

    recipe_dict = model_to_dict(new_recipe)

    recipe_dict['poster'].pop('password')

    return jsonify(
        data=recipe_dict,
        message="Successfully created recipe!",
        status=201
    ), 201


# recipe destroy route

@recipes.route('/<id>', methods=['DELETE'])
@login_required
def delete_recipe(id):

    try:
        recipe_to_delete = models.Recipe.get_by_id(id)

        if recipe_to_delete.poster.id == current_user.id:

            recipe_to_delete.delete_instance()

            return jsonify(
                data={},
                message="Successfully deleted recipe with the id of {}".format(id),
                status=200
            ), 200

        else:
            return jsonify(
                data={},
                message="Not your recipe!",
                status=403
            ), 403

    except models.DoesNotExist:
        return jsonify(
            data={},
            message="There's no recipe with that ID",
            status=404
        ), 404



# update route
@recipes.route('/<id>', methods=['PUT'])
@login_required
def update_recipe(id):
    payload = request.get_json()

    recipe_to_update = models.Recipe.get_by_id(id)

    if recipe_to_update.poster.id == current_user.id:

        if 'name' in payload:
            recipe_to_update.name = payload['name']
        if 'origin' in payload:
            recipe_to_update.origin = payload['origin']
        if 'ingredients' in payload:
            recipe_to_update.ingredients = payload['ingredients']
        if 'instructions' in payload:
            recipe_to_update.instructions = payload['instructions']

        recipe_to_update.save()

        updated_recipe_dict = model_to_dict(recipe_to_update)

        updated_recipe_dict['poster'].pop('password')

        return jsonify(
            data=updated_recipe_dict,
            message="Successfully updated the recipe with id of {}".format(id),
            status = 200
        ), 200

    else:
        return jsonify(
            data={},
            message="Not your recipe!!",
            status=403
        ), 403

@recipes.route('/<id>', methods=['GET'])
def show_recipe(id):
    recipe = models.Recipe.get_by_id(id)

    recipe_dict = model_to_dict(recipe)

    return jsonify(
        data=recipe_dict,
        message="Found recipe with id of {}".format(id),
        status=200
    ), 200
