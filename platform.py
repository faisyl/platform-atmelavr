# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from platformio.managers.platform import PlatformBase


class AtmelavrPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        if not variables.get("board"):
            return super(AtmelavrPlatform, self).configure_default_packages(
                variables, targets)

        build_core = variables.get(
            "board_build.core", self.board_config(variables.get("board")).get(
                "build.core", "arduino"))

        if "arduino" in variables.get(
                "pioframework", []) and build_core != "arduino":

            framework_package = "framework-arduino-avr-%s" % build_core.lower()
            if build_core in ("dtiny", "pro"):
                framework_package = "framework-arduino-avr-digistump"
            elif build_core in ("tiny", "tinymodern"):
                framework_package = "framework-arduino-avr-attiny"

            self.frameworks["arduino"]["package"] = framework_package
            self.packages[framework_package]["optional"] = False
            self.packages["framework-arduino-avr"]["optional"] = True

        upload_protocol = variables.get(
            "upload_protocol",
            self.board_config(variables.get("board")).get(
                "upload.protocol", ""))
        disabled_tools = ["tool-micronucleus", "tool-dwdebug"]
        required_tool = ""

        if upload_protocol in ["micronucleus", "dwdebug"]:
            disabled_tools = ["tool-avrdude"]

        if "fuses" in targets:
            required_tool = "tool-avrdude"

        if required_tool in self.packages:
            self.packages[required_tool]['optional'] = False

        for disabled_tool in disabled_tools:
            if disabled_tool in self.packages and disabled_tool != required_tool:
                del self.packages[disabled_tool]

        return super(AtmelavrPlatform, self).configure_default_packages(
            variables, targets)

    def on_run_err(self, line):  # pylint: disable=R0201
        # fix STDERR "flash written" for avrdude
        if "avrdude" in line:
            self.on_run_out(line)
        else:
            PlatformBase.on_run_err(self, line)
