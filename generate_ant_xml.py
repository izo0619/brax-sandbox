import typing as t


class Leg:
    def __init__(
        self,
        model_name,
        name,
        upper_leg,
        position=[0, 0, 0],
        size=0.08,
    ):
        self.model_name = model_name
        self.name = name
        self.position = position
        self.size = size
        self.geom = None
        self.upper_leg = upper_leg
        self.index_qpos = -1
        self.index_qvel = -1

    def get_xml(self):
        (xml, geom, joint, nb_bodies) = xml_templates.get_leg_xml(
            self.model_name,
            self.name,
            self.position,
            self.size,
            self.geom,
            self.upper_leg
        )
        return (xml, geom, joint, nb_bodies)


class Upper_Leg:
    def __init__(
        self,
        model_name,
        name,
        bottom_leg,
        position=[0, 0, 0],
        size=0.08,
    ):
        self.model_name = model_name
        self.name = name
        self.position = position
        self.size = size
        self.geom = None
        self.joint = None
        self.bottom_leg = bottom_leg
        self.index_qpos = -1
        self.index_qvel = -1

    def get_xml(self):
        (xml, geom, joint, nb_bodies) = xml_templates.get_leg_xml(
            self.model_name,
            self.name,
            self.position,
            self.size,
            self.geom,
            self.bottom_leg
        )
        return (xml, geom, joint, nb_bodies)


class Bottom_Leg:
    def __init__(
        self,
        model_name,
        name,
        position=[0, 0, 0],
        size=[0.03, 0.0007],
    ):
        self.model_name = model_name
        self.name = name
        self.position = position
        self.size = size
        self.geom = None
        self.joint = None
        self.index_qpos = -1
        self.index_qvel = -1

    def get_xml(self):
        (xml, geom, joint, nb_bodies) = xml_templates.get_leg_xml(
            self.model_name,
            self.name,
            self.position,
            self.size,
            self.geom,
        )
        return (xml, geom, joint, nb_bodies)


def generate_model(
    model_name: str,
    legs: t.Sequence[Leg] = [],
    gaps: t.Dict[str, t.Dict[str, float]] = defaults_gaps(),
) -> str:
    template = paths.get_main_template_xml()

    bodies = []
    index_qpos = 0
    index_qvel = 0

    # ball: instance of Ball (in this file)
    for leg in legs:
        xml, geom, joint, nb_bodies = leg.get_xml()
        bodies.append(xml)
        leg.index_qpos = index_qpos
        leg.index_qvel = index_qvel
        leg.geom = geom
        leg.joint = joint
        index_qpos += 7
        index_qvel += 6

    template = template.replace("<!-- bodies -->", "\n".join(bodies))

    if any([r.muscles for r in robots]):
        actuations = ["<tendon>"]
        for robot in robots:
            xml_tendon = paths.get_robot_tendon_xml(robot.name)
            actuations.append(xml_tendon)
        actuations.append("</tendon>")
        actuations.append("<actuator>")
        for robot in robots:
            xml_actuator = paths.get_robot_actuator_xml(robot.name)
            actuations.append(xml_actuator)
        actuations.append("</actuator>")
        template = template.replace(
            "<!-- actuations -->", "\n".join(actuations))

    contacts = xml_templates.get_contacts_xml(
        robots, balls, tables, solrefs, gaps)

    template = template.replace("<!-- contacts -->", contacts)

    path = paths.write_model_xml(model_name, template)

    return path
