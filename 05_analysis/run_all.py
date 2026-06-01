"""One-shot reproducible pipeline: base analysis + figures + advanced + tables."""
import figuras
import analisis_avanzado
import tablas_sintesis
import robustez

if __name__ == "__main__":
    figuras.main()            # analizar.main() + base figures F1-F6
    analisis_avanzado.main()  # F7-F10 + capa4b/c/d
    tablas_sintesis.main()    # T-A, T-B
    robustez.main()           # threshold sensitivity + bootstrap CIs
    print("\n[run_all] complete.")
