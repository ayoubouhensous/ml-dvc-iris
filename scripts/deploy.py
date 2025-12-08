from pathlib import Path
import json
import shutil

def load_json(path: Path):
    """Charge un fichier JSON et retourne un dictionnaire, ou None si le fichier n'existe pas."""
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)

def main():
    # Chemins
    metrics_eval_path = Path("metrics/eval_metrics.json")
    best_metrics_path = Path("metrics/best_metrics.json")
    model_path = Path("models/random_forest.pkl")
    production_model_path = Path("models/production_model.pkl")

    # 1. Charger les métriques
    metrics_eval = load_json(metrics_eval_path)
    if metrics_eval is None:
        print(f"Fichier {metrics_eval_path} introuvable.")
        return

    current_acc = metrics_eval.get("accuracy_full_data") or metrics_eval.get("accuracy_test")
    if current_acc is None:
        print("Accuracy introuvable dans les métriques.")
        return

    # 2. Charger les meilleures métriques connues
    best_metrics = load_json(best_metrics_path)
    best_acc = best_metrics.get("accuracy") if best_metrics else 0.0

    print(f"Accuracy courante: {current_acc}, meilleure accuracy connue: {best_acc}")

    # 3. Comparer et éventuellement promouvoir
    if current_acc > best_acc:
        # Copier le modèle
        production_model_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(model_path, production_model_path)
        print(f"Modèle promu vers {production_model_path}")

        # Mettre à jour les meilleures métriques
        best_metrics_new = {"accuracy": current_acc}
        best_metrics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(best_metrics_path, "w") as f:
            json.dump(best_metrics_new, f, indent=4)
        print(f"Meilleures métriques mises à jour dans {best_metrics_path}")
    else:
        print("Le modèle actuel n'améliore pas la meilleure accuracy, pas de déploiement.")

if __name__ == "__main__":
    main()
