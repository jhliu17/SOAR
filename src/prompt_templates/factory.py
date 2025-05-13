class PromptTemplateBase:
    def format_messages(self, slots: dict[str, str], **kwargs) -> list[dict[str, str]]:
        raise NotImplementedError

    def get_messages(self, *args, **kwargs) -> str:
        raise NotImplementedError


class RankedGeneNamesPromptTemplate(PromptTemplateBase):
    def format_messages(self, slots: dict[str, str], **kwargs) -> list[dict[str, str]]:
        formated_messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
            },
            {
                "role": "user",
                "content": f"Identify the cell type of {slots['tissue']} using the following markers, {slots['gene_names']}.",
            },
        ]

        return formated_messages

    def get_messages(
        self,
        tissue: str,
        list_of_genes: list[str],
        *args,
        **kwargs,
    ) -> list[dict[str, str]]:
        genes = ", ".join(list_of_genes)
        slots = {"tissue": tissue, "gene_names": genes}
        return self.format_messages(slots)


class ZeroShotRankedGeneNamesPromptTemplate(RankedGeneNamesPromptTemplate):
    @property
    def direct_answer_trigger_for_zeroshot(self):
        return "The most likely cell type (directly return one cell type name) is"

    def format_messages(self, slots: dict[str, str], **kwargs) -> list[dict[str, str]]:
        formated_messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": "You are a biology expert who always responds the cell type annotation result by carefully considering the markers provided by the user.",
            },
            {
                "role": "user",
                "content": f"Given the following markers [{slots['gene_names']}], what is the specific cell type in {slots['tissue']} corresponding to these markers? {self.direct_answer_trigger_for_zeroshot}",
            },
        ]

        return formated_messages


class ZeroShotCoTRankedGeneNamesPromptTemplate(ZeroShotRankedGeneNamesPromptTemplate):
    @property
    def cot_trigger(self):
        return "Let's think step by step."

    def direct_answer_trigger_for_zeroshot_cot(self, slots: dict[str, str]):
        return "In summary, the most likely cell type (directly return one cell type name) is"
        # return "Therefore, the cell type is"

    def format_messages(self, slots: dict[str, str], **kwargs) -> list[dict[str, str]]:
        if "reasoning" not in slots:
            formated_messages: list[dict[str, str]] = [
                {
                    "role": "system",
                    "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
                },
                {
                    "role": "user",
                    "content": f"Given the following markers [{slots['gene_names']}], what is the specific cell type in {slots['tissue']} corresponding to these markers? {self.cot_trigger}",
                },
            ]
        else:
            formated_messages: list[dict[str, str]] = [
                {
                    "role": "system",
                    "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
                },
                {
                    "role": "user",
                    "content": f"Given the following markers [{slots['gene_names']}], what is the specific cell type in {slots['tissue']} corresponding to these markers? {self.cot_trigger} {slots['reasoning']} {self.direct_answer_trigger_for_zeroshot_cot(slots)}",
                },
            ]

        return formated_messages

    def get_messages(
        self,
        tissue: str,
        list_of_genes: list[str],
        *args,
        **kwargs,
    ) -> list[dict[str, str]]:
        genes = ", ".join(list_of_genes)
        slots = {
            "tissue": tissue,
            "gene_names": genes,
        }

        if "reasoning" in kwargs:
            slots["reasoning"] = kwargs["reasoning"]
        return self.format_messages(slots)


class ZeroShotRankedGeneNamesPromptTemplateForSCACT(
    ZeroShotRankedGeneNamesPromptTemplate
):
    def direct_answer_trigger_for_zeroshot(self, slots: dict[str, str]):
        return f"The most likely specific cell type in {slots['tissue']} (directly return one cell type name) is"

    def format_messages(self, slots: dict[str, str], **kwargs) -> list[dict[str, str]]:
        formated_messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
            },
            {
                "role": "user",
                "content": f"Given the following markers [{slots['gene_names']}], what is the specific cell type in {slots['tissue']} corresponding to these markers? {self.direct_answer_trigger_for_zeroshot(slots)}",
            },
        ]

        return formated_messages


class ZeroShotCoTRankedGeneNamesPromptTemplateForSCACT(
    ZeroShotRankedGeneNamesPromptTemplate
):
    @property
    def cot_trigger(self):
        return "Let's think step by step."

    def direct_answer_trigger_for_zeroshot_cot(self, slots: dict[str, str]):
        return f"In summary, the most likely specific cell type in {slots['tissue']} (directly return one cell type name) is"
        # return "Therefore, the cell type is"

    def format_messages(self, slots: dict[str, str], **kwargs) -> list[dict[str, str]]:
        if "reasoning" not in slots:
            formated_messages: list[dict[str, str]] = [
                {
                    "role": "system",
                    "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
                },
                {
                    "role": "user",
                    "content": f"Given the following markers [{slots['gene_names']}], what is the specific cell type in {slots['tissue']} corresponding to these markers? {self.cot_trigger}",
                },
            ]
        else:
            formated_messages: list[dict[str, str]] = [
                {
                    "role": "system",
                    "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
                },
                {
                    "role": "user",
                    "content": f"Given the following markers [{slots['gene_names']}], what is the specific cell type in {slots['tissue']} corresponding to these markers? {self.cot_trigger} {slots['reasoning']} {self.direct_answer_trigger_for_zeroshot_cot(slots)}",
                },
            ]

        return formated_messages

    def get_messages(
        self,
        tissue: str,
        list_of_genes: list[str],
        *args,
        **kwargs,
    ) -> list[dict[str, str]]:
        genes = ", ".join(list_of_genes)
        slots = {
            "tissue": tissue,
            "gene_names": genes,
        }

        if "reasoning" in kwargs:
            slots["reasoning"] = kwargs["reasoning"]
        return self.format_messages(slots)


class FewShotRankedGeneNamesPromptTemplate(ZeroShotCoTRankedGeneNamesPromptTemplate):
    def format_messages(self, slots: dict[str, str], **kwargs) -> list[dict[str, str]]:
        demo_messages = []
        for demo in slots["demo"]:
            gene_names = ", ".join(demo["gene_names"])
            question = f"Question: Given the following markers [{gene_names}], what is the cell type in {demo['tissue']} corresponding to these markers?"
            reasoning = demo["reasoning"]
            answer = f"In summary, the most likely cell type (one cell type name) is {demo['cell_type']}"
            demo_messages.append(
                f"{question}\n{self.cot_trigger}\n{reasoning}\n{answer}"
            )

        demo_str = "\n\n".join(demo_messages)
        formated_messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": "You are a biology expert who always responds the cell type annotation result by carefully consiering the markers provided by the user.",
            },
            {
                "role": "user",
                "content": f"{demo_str}\n\nQuestion: Given the following markers [{slots['gene_names']}], what is the specific cell type in {slots['tissue']} corresponding to these markers?",
            },
        ]

        return formated_messages

    def get_messages(
        self,
        tissue: str,
        list_of_genes: list[str],
        *args,
        **kwargs,
    ) -> list[dict[str, str]]:
        if "demo" not in kwargs:
            raise ValueError("The 'demo' key is missing in the slots")

        demo = kwargs["demo"]
        genes = ", ".join(list_of_genes)
        slots = {"tissue": tissue, "gene_names": genes, "demo": demo}
        return self.format_messages(slots)
