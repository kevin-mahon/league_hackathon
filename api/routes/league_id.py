from flask import Blueprint, request, jsonify
from api.utils.validator import validate_field, ValidationError
import logging

logger = logging.getLogger(__name__)

league_id_blueprint = Blueprint('league-id', __name__)

@league_id_blueprint.route('/league-id', methods=['GET'])
def index():
    league_id = request.args.get("league_id")
    try:
        league_id = validate_field(
            league_id,
            str,
            required=True,
            min_length=10,
            max_length=20
        )

        
    except ValidationError as e:
        logger.error(f"Validation error: {e.message}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({"error": "Something went wrong"}), 500
    
    return jsonify({"message": league_id}), 200


