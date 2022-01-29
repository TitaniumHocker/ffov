import re
import os
import typing as t

from ffov.setters.base import FovSetter


class NewVegasFovSetter(FovSetter):

    ini = "Fallout_default.ini"
    exe = "FalloutNV.exe"
    pattern_template = r"^({}=\d+(\.\d+)?)$"

    def read(self) -> str:
        with open(os.path.join(self.gamepath, self.ini), "rt") as fh:
            return fh.read()
    
    def write(self, data: str):
        with open(os.path.join(self.gamepath, self.ini), "wt") as fh:
            fh.write(data)
    
    def getfovs(self) -> t.Tuple[float, float, float]:
        config = self.read()
        fov = float(re.findall(self.pattern_template.format("fDefault1stPersonFOV"), config, re.M)[0][0].split("=")[-1])
        pipfov = float(re.findall(self.pattern_template.format("fPipboy1stPersonFOV"), config, re.M)[0][0].split("=")[-1])
        termfov = float(re.findall(self.pattern_template.format("fRenderedTerminalFOV"), config, re.M)[0][0].split("=")[-1])
        return fov, pipfov, termfov

    def setfovs(
        self,
        fov: t.Union[int, float],
        pipfov: t.Union[int, float],
        termfov: t.Union[int, float]
    ) -> t.Tuple[bool, t.Optional[str]]:
        config = self.read()
        if "fDefaultWorldFOV" not in config:
            config = config.replace("fDefaultFOV", "fDefaultWorldFOV=75.0\nfDefaultFOV")
        
        for find, replace in (
            ("fDefaultFOV", f"fDefaultFOV={float(fov)}"),
            ("fDefaultWorldFOV", f"fDefaultWorldFOV={float(fov)}"),
            ("fDefault1stPersonFOV", f"fDefault1stPersonFOV={float(fov)}"),
            ("fPipboy1stPersonFOV", f"fPipboy1stPersonFOV={float(pipfov)}"),
            ("fRenderedTerminalFOV", f"fRenderedTerminalFOV={float(termfov)}"),
        ):
            config = re.sub(self.pattern_template.format(find), replace, config, 1, re.M)

        self.write(config)
        return True, None
