/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { SectionAndNoteListRenderer } from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";

// Speichere die Referenz zu den Originalmethoden
const originalSetup = SectionAndNoteListRenderer.prototype.setup;
const originalGetCellClass = SectionAndNoteListRenderer.prototype.getCellClass;
const originalGetSectionColumns = SectionAndNoteListRenderer.prototype.getSectionColumns;

// Patche die bestehende Klasse, um das neue Feld hinzuzufügen
patch(SectionAndNoteListRenderer.prototype, {
    setup() {
        // Rufe die Original-Setup-Methode auf
        originalSetup.call(this);
        console.log("ExtendedSectionAndNoteListRenderer setup called");  // Debugging-Ausgabe
        this.newField = "section_for_signature"; // Hier den Namen deines neuen Feldes einfügen
    },

    getCellClass(column, record) {
        const classNames = originalGetCellClass.call(this, column, record);
        console.log("getCellClass called, column:", column, "record:", record);  // Debugging-Ausgabe
        if (this.isSectionOrNote(record) && column.widget !== "handle" && column.name !== this.titleField && column.name !== this.newField) {
            return `${classNames} o_hidden`;
        }
        return classNames;
    },

    getSectionColumns(columns) {
        console.log("getSectionColumns called, columns:", columns);  // Debugging-Ausgabe
        const sectionCols = columns.filter((col) => col.widget === "handle" || col.name === this.titleField || col.name === this.newField);
        console.log("sectionCols:", sectionCols);  // Debugging-Ausgabe
        return columns.map((col) => {
            if (col.name === this.titleField || col.name === this.newField) {
                return { ...col, colspan: 1 }; // Setzen Sie colspan auf 1, um eine gleichmäßige Verteilung sicherzustellen
            } else if (sectionCols.includes(col)) {
                return { ...col, colspan: columns.length - sectionCols.length + 1 }; // Setzen Sie colspan für andere Felder
            } else {
                return { ...col, colspan: 0 }; // Verbergen Sie andere Felder
            }
        });
    }
});

console.log("Extended SectionAndNoteListRenderer registered");  // Debugging-Ausgabe


/** @odoo-module

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { SectionAndNoteListRenderer } from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { TextField, ListTextField } from "@web/views/fields/text/text_field";
import { CharField } from "@web/views/fields/char/char_field";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useEffect } from "@odoo/owl";

export class ExtendedSectionAndNoteListRenderer extends SectionAndNoteListRenderer {
    setup() {
        super.setup();
        this.newField = "section_for_signature"; // Hier den Namen deines neuen Feldes einfügen
         useEffect(
                      () => [this.props.list.editedRecord]
        )
        console.log("ExtendedSectionAndNoteListRenderer setup called");  // Debugging-Ausgabe
    }

    getCellClass(column, record) {
        console.log("ExtendedSectionAndNoteListRenderer getCellClass called");
        const classNames = super.getCellClass(column, record);
        if (this.isSectionOrNote(record) && column.widget !== "handle" && column.name !== this.titleField && column.name !== this.newField) {
            return `${classNames} o_hidden`;
        }
        return classNames;
    }

    getSectionColumns(columns) {
        console.log("ExtendedSectionAndNoteListRenderer getSectionColumns called");  // Debugging-Ausgabe
        const sectionCols = columns.filter((col) => col.widget === "handle" || col.type === "field" && (col.name === this.titleField || col.name === this.newField));
        return sectionCols.map((col) => {
            if (col.name === this.titleField) {
                return { ...col, colspan: columns.length - sectionCols.length + 1 };
            } else {
                return { ...col };
            }
        });
    }
}

registry.category('fields').add('section_and_note_text_kas', {
    ...x2ManyField,
    component: X2ManyField,
    Renderer: ExtendedSectionAndNoteListRenderer,
    additionalClasses: [...x2ManyField.additionalClasses || [], "o_field_one2many"],
});

console.log("Extended SectionAndNoteListRenderer registered");  // Debugging-Ausgabe
**/