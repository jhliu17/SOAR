samples = [
    {
        "index": 45,
        "sample": {
            "index": 45,
            "dataset": "Azimuth",
            "tissue": "Motor Cortex",
            "genes": [
                "CNR1",
                "SLC8A1",
                "ASIC2",
                "CXCL14",
                "MAML3",
                "ADARB2",
                "NPAS3",
                "CNTN5",
                "FSTL5",
                "SNCG",
            ],
            "label": "Sncg+ GABAergic neuron",
            "label_cl": "sncg GABAergic cortical interneuron",
            "label_id": "CL:4023015",
            "broadtype": "neuron",
            "demo": "",
        },
        "messages": [
            {
                "generated_text": [
                    {
                        "role": "system",
                        "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
                    },
                    {
                        "role": "user",
                        "content": "Given the following markers [CNR1, SLC8A1, ASIC2, CXCL14, MAML3, ADARB2, NPAS3, CNTN5, FSTL5, SNCG], what is the cell type in Motor Cortex corresponding to these markers? Let's think step by "
                        "step. To determine the cell type in the motor cortex that corresponds to the list of markers you've provided, we need to consider each marker and its known expression patterns. Here’s how we "
                        "can break it down:\n"
                        "\n"
                        "1. **CNR1 (Cannabinoid receptor 1)**: This receptor is widely expressed in the brain, including in neurons and glial cells. However, in specific contexts, it can be more enriched in certain "
                        "neuronal populations.\n"
                        "\n"
                        "2. **SLC8A1 (Sodium/calcium exchanger 1)**: This transporter plays a role in calcium homeostasis and is broadly expressed in neurons, but its specific expression pattern in different brain "
                        "regions might vary.\n"
                        "\n"
                        "3. **ASIC2 (Acid-sensing ion channel 2)**: Involved in pH sensing, this protein is found in various neuronal types, particularly those involved in sensory processing.\n"
                        "\n"
                        "4. **CXCL14 (Chemokine (C-X-C motif) ligand 14)**: This chemokine is involved in immune responses and has been found in microglia and astrocytes, as well as some neuronal populations.\n"
                        "\n"
                        "5. **MAML3 (Mastermind-like 3)**: This protein is involved in Notch signaling and has been implicated in neural development. Its expression is complex and can vary across different cell "
                        "types.\n"
                        "\n"
                        "6. **ADARB2 (Adenosine deaminase acting on RNA 2)**: This enzyme modifies RNA and is generally associated with neuronal cells, particularly in the context of learning and memory.\n"
                        "\n"
                        "7. **NPAS3 (Neuronal PAS domain protein 3)**: This transcription factor is crucial for neuronal development and function, often expressed in GABAergic interneurons.\n"
                        "\n"
                        "8. **CNTN5 (Contactin 5)**: A member of the immunoglobulin superfamily, this protein is involved in axon guidance and synaptogenesis, typically found in neurons.\n"
                        "\n"
                        "9. **FSTL5 (Follistatin-like 5)**: This protein has roles in inhibiting growth factors and is expressed in various tissues, including the brain, where it might be involved in neurogenesis or "
                        "neuronal maintenance.\n"
                        "\n"
                        "10. **SNCG (Gamma-synuclein)**: This protein is expressed in neurons and is particularly abundant in the motor cortex and other areas of the brain involved in movement.\n"
                        "\n"
                        "Considering the markers together, there's a strong neuronal component, which is expected given the location in the motor cortex. Markers like CNR1, ASIC2, NPAS3, CNTN5, and SNCG suggest a "
                        "neuronal identity, possibly GABAergic interneurons or specific subtypes of excitatory neurons given the role of these genes in neurotransmission and neuronal function. \n"
                        "\n"
                        "However, without a definitive database or study specifically linking these markers to a particular cell type in the motor cortex, we can only infer based on their known functions and "
                        "expression patterns. The combination of these markers suggests a neuronal cell type, potentially with a specialization in motor or sensory processing given the presence of ASIC2 and SNCG. \n"
                        "\n"
                        "For a precise cell type annotation, one would typically rely on single-cell RNA sequencing data from the motor cortex, comparing the expression profiles of individual cells to the markers "
                        "listed here. If such data were available and showed a significant enrichment of these markers in a specific cell population, that would provide a more concrete answer. In summary, the most "
                        "likely cell type (one cell type name) is",
                    },
                    {
                        "role": "assistant",
                        "content": "**GABAergic Interneuron**.\n"
                        "\n"
                        "The presence of markers such as CNR1, NPAS3, and CNTN5, which are known to be highly expressed in GABAergic interneurons, along with others that are broadly neuronal but contribute to the "
                        "specificity of these interneurons' functions, suggests that this cell type is the most consistent with the marker profile provided. GABAergic interneurons play critical roles in the motor "
                        "cortex, particularly in modulating the activity of excitatory neurons and coordinating motor output.",
                    },
                ]
            }
        ],
    },
    {
        "index": 46,
        "sample": {
            "index": 46,
            "dataset": "Azimuth",
            "tissue": "Motor Cortex",
            "genes": [
                "GRIK1",
                "RALYL",
                "SST",
                "TRHDE",
                "GRID2",
                "NXPH1",
                "COL25A1",
                "SLC8A1",
                "SOX6",
                "ST6GALNAC5",
            ],
            "label": "Sst+ GABAergic neuron",
            "label_cl": "sst GABAergic cortical interneuron",
            "label_id": "CL:4023017",
            "broadtype": "neuron",
            "demo": "",
        },
        "messages": [
            {
                "generated_text": [
                    {
                        "role": "system",
                        "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
                    },
                    {
                        "role": "user",
                        "content": "Given the following markers [GRIK1, RALYL, SST, TRHDE, GRID2, NXPH1, COL25A1, SLC8A1, SOX6, ST6GALNAC5], what is the cell type in Motor Cortex corresponding to these markers? Let's think step "
                        "by step. To determine the cell type in the motor cortex that corresponds to the markers you've provided, we need to consider each marker and its typical expression pattern. Here's how we can "
                        "break it down:\n"
                        "\n"
                        "1. **GRIK1 (Glutamate receptor, ionotropic, kainate 1)** - This marker is associated with glutamatergic neurons, particularly in the brain regions involved in learning and memory.\n"
                        "\n"
                        "2. **RALYL (Ras-like, estrogen-regulated, Y-linked)** - While this gene has been implicated in various functions including cell proliferation and development, its specific role in identifying "
                        "a cell type is less clear compared to others listed here.\n"
                        "\n"
                        "3. **SST (Somatostatin)** - This is a marker for somatostatin-expressing interneurons, which are GABAergic neurons found throughout the brain, including the motor cortex.\n"
                        "\n"
                        "4. **TRHDE (Triiodothyronine deiodinase)** - This enzyme is involved in thyroid hormone metabolism but is not typically used as a specific marker for neuronal subtypes.\n"
                        "\n"
                        "5. **GRID2 (Glutamate receptor, ionotropic, delta 2)** - This gene encodes for a subunit of the delta-type glutamate receptors, which are found in various neuronal populations, including "
                        "those in the motor cortex.\n"
                        "\n"
                        "6. **NXPH1 (Neurexophilin 1)** - This gene encodes for a protein involved in synaptic function and is expressed in neurons.\n"
                        "\n"
                        "7. **COL25A1 (Collagen, type XXV, alpha 1)** - This gene is part of the collagen family, and while it has roles in development, it is not specifically tied to a particular cell type in the "
                        "nervous system.\n"
                        "\n"
                        "8. **SLC8A1 (Solute carrier family 8 member 1)** - This gene encodes for a sodium/calcium exchanger, which is important in regulating intracellular calcium levels and is broadly expressed "
                        "across many cell types, including neurons.\n"
                        "\n"
                        "9. **SOX6 (SRY-box transcription factor 6)** - This transcription factor is crucial for the specification of oligodendrocytes and motor neurons during development.\n"
                        "\n"
                        "10. **ST6GALNAC5 (ST6 beta-galactoside alpha-2,6-sialyltransferase 5)** - This enzyme is involved in glycosylation processes and is not typically used as a specific marker for neuronal "
                        "subtypes.\n"
                        "\n"
                        "Considering the markers above, the combination of **SST**, **GRID2**, and **SOX6** stands out as particularly relevant for identifying cell types in the motor cortex. **SST** marks inhibitory "
                        "interneurons, **GRID2** is related to glutamatergic signaling, and **SOX6** is involved in the development of motor neurons. However, **SOX6** is perhaps the most indicative here, given its "
                        "role in specifying motor neurons.\n"
                        "\n"
                        "Thus, based on the markers provided, the cell type in the motor cortex that these markers likely correspond to is **motor neurons** or possibly a mixed population that includes motor neurons "
                        "and certain interneurons. However, it's important to note that the identification of cell types from markers alone can be complex due to overlapping expression patterns and the possibility of "
                        "co-expression in different cell types. Further validation through additional markers or functional assays might be necessary to confirm the exact cell type. In summary, the most likely cell "
                        "type (one cell type name) is",
                    },
                    {
                        "role": "assistant",
                        "content": "motor neurons. However, considering the presence of SST, a marker for somatostatin-expressing interneurons, it suggests a mixed population that could include both motor neurons and specific "
                        "inhibitory interneurons within the motor cortex. The inclusion of SOX6, which is critical for motor neuron specification, strongly supports the identification of motor neurons as a primary "
                        "component of this cell population.",
                    },
                ]
            }
        ],
    },
    {
        "index": 47,
        "sample": {
            "index": 47,
            "dataset": "Azimuth",
            "tissue": "Motor Cortex",
            "genes": [
                "NPY",
                "FAM46A",
                "STAC",
                "OTOF",
                "NPY2R",
                "CRHBP",
                "ANKRD34B",
                "NOS1",
                "SST",
                "CHODL",
            ],
            "label": "Sst+ Chodl+ GABAergic neuron",
            "label_cl": "sst chodl GABAergic cortical interneuron",
            "label_id": "CL:4023121",
            "broadtype": "neuron",
            "demo": "",
        },
        "messages": [
            {
                "generated_text": [
                    {
                        "role": "system",
                        "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
                    },
                    {
                        "role": "user",
                        "content": "Given the following markers [NPY, FAM46A, STAC, OTOF, NPY2R, CRHBP, ANKRD34B, NOS1, SST, CHODL], what is the cell type in Motor Cortex corresponding to these markers? Let's think step by "
                        "step. To determine the cell type in the motor cortex that corresponds to the markers you've listed, we need to consider each marker and its known associations with specific cell types in the "
                        "brain. Here’s a breakdown of the markers:\n"
                        "\n"
                        "1. **NPY (Neuropeptide Y)**: This is a neurotransmitter that is often expressed in GABAergic interneurons. In particular, it is associated with a subtype of interneurons called NPY-positive "
                        "interneurons.\n"
                        "\n"
                        "2. **FAM46A (Family With Sequence Similarity 46 Member A)**: This gene's function is not well characterized, but it has been implicated in amyotrophic lateral sclerosis (ALS). Its expression "
                        "pattern in specific cell types within the motor cortex is not widely documented.\n"
                        "\n"
                        "3. **STAC (SH3 And cysteine-rich domain)**: This protein is involved in cell adhesion and signal transduction. Its expression in specific neuronal subtypes is not extensively studied.\n"
                        "\n"
                        "4. **OTOF (Otoferlin)**: This gene encodes a protein that plays a role in neurotransmitter release at synapses. It is primarily associated with auditory hair cells but has also been found in "
                        "other neurons.\n"
                        "\n"
                        "5. **NPY2R (Neuropeptide Y Receptor Type 2)**: This receptor binds to neuropeptide Y, which suggests its presence in neurons that respond to NPY signaling. This could include various "
                        "interneuron subtypes.\n"
                        "\n"
                        "6. **CRHBP (Corticotropin-releasing hormone binding protein)**: This protein binds to corticotropin-releasing hormone (CRH), which is involved in stress responses. Its expression can be seen "
                        "in various parts of the brain, including the hypothalamus and cerebral cortex.\n"
                        "\n"
                        "7. **ANKRD34B (Ankyrin Repeat Domain 34B)**: This gene is less studied in the context of neural cell types. It contains ankyrin repeats, which are involved in protein-protein interactions, "
                        "but its specific role in neurons is unclear.\n"
                        "\n"
                        "8. **NOS1 (Nitric Oxide Synthase 1)**: This enzyme catalyzes the production of nitric oxide, a signaling molecule in the nervous system. NOS1 is expressed in both neurons and glial cells, but "
                        "in the context of the motor cortex, it is more commonly associated with specific subtypes of neurons.\n"
                        "\n"
                        "9. **SST (Somatostatin)**: This hormone is also produced by certain GABAergic interneurons, particularly somatostatin-positive interneurons, which play a critical role in modulating neuronal "
                        "activity.\n"
                        "\n"
                        "10. **CHODL (Chondroitin Sulphate N-Acetylgalactosaminyltransferase Like)**: This enzyme is involved in the biosynthesis of chondroitin sulfate proteoglycans, which are components of the "
                        "extracellular matrix. Its role in defining specific cell types is less clear.\n"
                        "\n"
                        "Given this list, the most consistent markers for identifying a cell type in the motor cortex are NPY, NPY2R, and SST, which point towards GABAergic interneurons, specifically NPY- and "
                        "SST-positive interneurons. These interneurons are crucial for regulating the activity of pyramidal cells and maintaining proper network function in the motor cortex.\n"
                        "\n"
                        "However, the presence of markers like NOS1 and possibly CRHBP could indicate a more specific subset of interneurons or a mix of different interneuron subtypes that are present in the motor "
                        "cortex. The other markers do not provide strong evidence for a specific cell type due to their less defined roles in neuronal subtyping.\n"
                        "\n"
                        "In conclusion, based on the markers provided, the cell type in the motor cortex likely corresponds to a subtype of GABAergic interneurons, potentially enriched for NPY- and SST-positive "
                        "interneurons. Further refinement would require additional markers that are more specifically associated with distinct interneuron subtypes within the motor cortex. In summary, the most likely "
                        "cell type (one cell type name) is",
                    },
                    {
                        "role": "assistant",
                        "content": "GABAergic interneurons, specifically those that are NPY- and SST-positive, given the markers you've provided. These interneurons play a critical role in modulating circuit activity in the "
                        "motor cortex.",
                    },
                ]
            }
        ],
    },
]
