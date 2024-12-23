import { TbRectangle } from "react-icons/tb";
import { IoMdDownload } from "react-icons/io";
import { FaLongArrowAltRight } from "react-icons/fa";
import { LuPencil } from "react-icons/lu";
import { GiArrowCursor } from "react-icons/gi";
import { FaRegCircle } from "react-icons/fa6";
import {
    Arrow,
    Circle,
    Layer,
    Line,
    Rect,
    Stage,
    Transformer,
} from "react-konva";
import { useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { ACTIONS } from "./Constants";
import MyButton from "../../components/UI/button/MyButton.jsx";

export default function ElementsField() {
    const stageRef = useRef();
    const [action, setAction] = useState(ACTIONS.SELECT);
    const [fillColor, setFillColor] = useState("#4676D7");
    const [rectangles, setRectangles] = useState([]);
    const [arrows, setArrows] = useState([]);

    const strokeColor = "#000";
    const isPaining = useRef();
    const currentShapeId = useRef();
    const transformerRef = useRef();

    const isDraggable = action === ACTIONS.SELECT;

    function onPointerDown() {
        if (action === ACTIONS.SELECT) return;

        const stage = stageRef.current;
        const { x, y } = stage.getPointerPosition();
        const id = uuidv4();

        currentShapeId.current = id;
        isPaining.current = true;

        switch (action) {
            case ACTIONS.RECTANGLE:
                setRectangles((rectangles) => [
                    ...rectangles,
                    {
                        id,
                        x,
                        y,
                        height: 20,
                        width: 20,
                        fillColor,
                    },
                ]);
                break;
            case ACTIONS.ARROW:
                setArrows((arrows) => [
                    ...arrows,
                    {
                        id,
                        points: [x, y, x + 20, y + 20],
                        fillColor,
                    },
                ]);
                break;
        }
    }
    function onPointerMove() {
        if (action === ACTIONS.SELECT || !isPaining.current) return;

        const stage = stageRef.current;
        const { x, y } = stage.getPointerPosition();

        switch (action) {
            case ACTIONS.RECTANGLE:
                setRectangles((rectangles) =>
                    rectangles.map((rectangle) => {
                        if (rectangle.id === currentShapeId.current) {
                            return {
                                ...rectangle,
                                width: x - rectangle.x,
                                height: y - rectangle.y,
                            };
                        }
                        return rectangle;
                    })
                );
                break;
            case ACTIONS.ARROW:
                setArrows((arrows) =>
                    arrows.map((arrow) => {
                        if (arrow.id === currentShapeId.current) {
                            return {
                                ...arrow,
                                points: [
                                    arrow.points[0],
                                    arrow.points[1],
                                    x,
                                    y,
                                ],
                            };
                        }
                        return arrow;
                    })
                );
                break;
        }
    }

    function onPointerUp() {
        isPaining.current = false;
    }

    function onClick(e) {
        if (action !== ACTIONS.SELECT) return;
        const target = e.currentTarget;
        transformerRef.current.nodes([target]);
    }

    return (
        <>
            <div className="absolute top-0 z-10 w-full py-2">
                {/* Controls */}
                <div onClick={() => setAction(ACTIONS.SELECT)}>
                    <MyButton>
                        <GiArrowCursor size={"2rem"} />
                    </MyButton>
                </div>
                <div onClick={() => setAction(ACTIONS.RECTANGLE)}>
                    <MyButton>
                        {" "}
                        <TbRectangle size={"2rem"} />
                    </MyButton>
                </div>
                <div onClick={() => setAction(ACTIONS.ARROW)}>
                    <MyButton>
                        <FaLongArrowAltRight size={"2rem"} />
                    </MyButton>
                </div>
            </div>
            <div>
                {/* Canvas */}
                <Stage
                    ref={stageRef}
                    width={window.innerWidth}
                    height={window.innerHeight}
                    onPointerDown={onPointerDown}
                    onPointerMove={onPointerMove}
                    onPointerUp={onPointerUp}
                >
                    <Layer>
                        <Rect
                            x={0}
                            y={0}
                            height={window.innerHeight}
                            width={window.innerWidth}
                            fill="#ffffff"
                            id="bg"
                            onClick={() => {
                                transformerRef.current.nodes([]);
                            }}
                        />
                        {rectangles.map((rectangle) => (
                            <Rect
                                key={rectangle.id}
                                x={rectangle.x}
                                y={rectangle.y}
                                stroke={strokeColor}
                                strokeWidth={2}
                                fill={rectangle.fillColor}
                                height={rectangle.height}
                                width={rectangle.width}
                                draggable={isDraggable}
                                onClick={onClick}
                            />
                        ))}
                        {arrows.map((arrow) => (
                            <Arrow
                                key={arrow.id}
                                points={arrow.points}
                                stroke={strokeColor}
                                strokeWidth={2}
                                fill={arrow.fillColor}
                                draggable={isDraggable}
                                onClick={onClick}
                            />
                        ))}
                        <Transformer ref={transformerRef} />
                    </Layer>
                </Stage>
            </div>
        </>
    );
}
