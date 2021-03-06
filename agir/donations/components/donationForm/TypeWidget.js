import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";

import { FlexContainer } from "./elements";

const TypeButtonContainer = styled.label`
  display: flex;
  justify-content: center;
  align-items: center;

  opacity: 1;
  margin: 10px;
  font-weight: bold;
  min-width: 200px;
  padding: 1em;
  border: 1px solid;
  padding: 1em;

  cursor: pointer;

  color: ${({ checked }) => (checked ? "#fff" : "#333")};
  background-color: ${({ checked }) => (checked ? "#c9462c" : "#fff")};
  border-color: ${({ checked }) => (checked ? "#b43f27" : "#adadad")};

  :hover {
    background-color: ${({ checked }) => (checked ? "#9f3723" : "#e6e6e6")};
    border-color: ${({ checked }) => (checked ? "#822d1c" : "#adadad")};
  }

  & > * {
    text-align: center;
    padding: 0 20px;
  }

  & > div + div {
    border-left: 1px solid #aaa;
  }
`;

const TypeButton = ({ label, onChange, icon, checked }) => (
  <TypeButtonContainer checked={checked}>
    <div>
      <input type="radio" onChange={onChange} checked={checked} />
    </div>
    <div>
      <div>
        <i className={`fa fa-${icon || "arrow-right"}`} />
      </div>
      <div>{label}</div>
    </div>
  </TypeButtonContainer>
);
TypeButton.propTypes = {
  label: PropTypes.string,
  onChange: PropTypes.func,
  icon: PropTypes.string,
  checked: PropTypes.bool,
};

const TypeWidget = ({ typeChoices, type, onTypeChange }) => (
  <FlexContainer justifyContent="center">
    {typeChoices.map(({ label, value, icon }) => (
      <TypeButton
        key={value}
        onChange={() => onTypeChange(value)}
        checked={type === value}
        label={label}
        icon={icon}
      />
    ))}
  </FlexContainer>
);

TypeWidget.propTypes = {
  type: PropTypes.string,
  typeChoices: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string,
      label: PropTypes.string,
    }).isRequired
  ),
  onTypeChange: PropTypes.func,
};

export default TypeWidget;
